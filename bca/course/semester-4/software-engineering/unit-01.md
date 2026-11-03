---
subject: Software Engineering
grade: BCA Semester 4
unit: 1
title: Introduction to Software Engineering
hours: 4
area: BCA 252 · Software Engineering · Unit 1
---

In 1968 a NATO conference in Garmisch coined the phrase "software engineering" because large software projects were routinely late, over budget and wrong; the situation was called the *software crisis*. Fifty years on, the Nepali government portals, bank systems and apps we depend on still fail for the same reasons: unclear requirements, poor estimates and weak process. This unit defines software, its attributes and the field built to address these problems.

::: key What this unit gives you
- Definition and types of software; characteristics and attributes of good software.
- Definition of software engineering, its costs and key challenges; system engineering versus software engineering.
- Professional practice and ethics.
:::

## 1.1 What is software?

**Software** is (1) instructions (programs) that provide desired function when executed, (2) data structures that let programs manipulate information, and (3) documentation describing their operation and use. A program is not a software *product*: a product has documentation, tests, installation and support, and is meant for users other than its author.

### Types of software

| Type | Description | Examples |
|---|---|---|
| **System software** | serves other programs | operating systems, compilers, drivers |
| **Application software** | solves a specific business or personal need | accounting, hospital management, a college result system |
| **Engineering/scientific** | numerical computation | CAD, simulation, MATLAB-like tools |
| **Embedded software** | resides in a device | washing machine, ABS controller |
| **Web/mobile applications** | delivered over the network or on phones | e-Sewa-style wallets, ride-hailing apps |
| **Artificial intelligence software** | uses non-numerical algorithms | expert systems, machine-learning services |
| **Product-line software** | a base shared by many customers | ERP, office suites |

Software can also be **generic** (produced for an open market, the developer owns the specification) or **custom/bespoke** (written for one client, the client owns the specification). Most revenue is in generic products, but most Nepali software work is custom.

### Characteristics of software

Software differs from hardware: (1) it is **developed or engineered, not manufactured**, so the cost lies in design, not copying; (2) it **does not wear out**; but it **deteriorates** as changes introduce defects (the failure-rate curve has spikes after every change instead of a bathtub); (3) most software is still **custom-built** rather than assembled from components, though reuse is increasing.

## 1.2 Attributes of good software

A good product delivers the required functionality *and* these non-functional attributes:

| Attribute | Meaning |
|---|---|
| **Maintainability** | can be evolved as needs change; the most important attribute because change is inevitable |
| **Dependability and security** | reliable, safe, and secure against malicious misuse |
| **Efficiency** | does not waste memory or processor time; response time, utilisation |
| **Acceptability** | usable, understandable and compatible with the users' systems |

## 1.3 Software engineering defined

> **Software engineering** is the application of a systematic, disciplined, quantifiable approach to the development, operation and maintenance of software (IEEE).

It is an *engineering* discipline: it uses theories, methods and tools but applies them selectively, within organisational and financial constraints, to produce a working solution. It concerns *all* aspects of production, from specification to maintenance, not just coding, and includes project management and tools.

**Software engineering versus computer science.** Computer science studies theory and fundamentals (algorithms, complexity); software engineering is about the practicalities of producing useful software. **Software engineering versus system engineering.** System engineering covers *whole* systems of hardware, software, people and processes (an ATM network, an airport) and decides which functions go to software; software engineering is concerned with the software part, after that decision. System engineers must manage emergent properties (reliability, safety) that depend on all parts together.

## 1.4 Software engineering costs

Roughly 60 % of costs are development costs and 40 % testing costs. For *custom* software, the **evolution (maintenance) costs often exceed development costs**, commonly by a factor of 2 to 4 over the product's life, and for long-lived systems a majority of the total. Costs depend on the process, the type of system and the dependability required: a safety-critical system costs far more per line than a prototype. Costs vary with project phase: a fault found during maintenance costs many times more to fix than one found during specification (Unit 3 quotes the typical figure of 50 to 100 times in the classic studies; the exact factor varies widely by project).

Estimation techniques that put numbers on these costs (COCOMO, function points) and a verified worked example appear in Unit 8.

## 1.5 Key challenges

- **Heterogeneity**: systems must run across different platforms, devices and legacy systems.
- **Business and social change**: delivery must be faster than the business can change; old systems must be adapted.
- **Security and trust**: software is attacked constantly, and users must trust it.
- **Scale**: from small embedded to Internet-scale systems.
- **Time to delivery** under pressure from competition.

## 1.6 Professional practice and ethics

Software engineering involves responsibilities beyond technical skill: **confidentiality** (respect the client's data), **competence** (do not accept work beyond your ability), **intellectual property** (respect licences and copyright), and **avoid computer misuse** (no unauthorised access, no malware). The joint **ACM/IEEE Software Engineering Code of Ethics** sets eight principles: *Public* (act in the public interest), *Client and Employer*, *Product* (high professional standards), *Judgment*, *Management*, *Profession*, *Colleagues*, and *Self* (lifelong learning). When the public interest and the employer conflict, the public interest comes first. In Nepal the *Electronic Transactions Act 2063* criminalises unauthorised access and cyber crimes, and the Individual Privacy Act 2075 protects personal data, so engineers need to know the local legal framework too.

::: example An ethical dilemma
A bank's developer finds an unreported bug that, under rare conditions, credits interest twice. The manager says to ignore it since "nobody has noticed". Under the code of ethics, the engineer must report the defect and refuse to conceal it: public and client interest outweigh the schedule. Escalate to a higher manager, document the report, and decline to participate if the matter is left unresolved.
:::

## 1.7 Software failures, real photographs and the cost of change

Software engineering exists because software fails in expensive ways. Plate 1.1 shows three pieces of evidence from the history of the subject, and Plate 1.2 shows a failure that came from a single unit mix-up. Figures 1.1 to 1.3 then explain *why* the same kind of fault costs more the later it is found, why software behaves differently from hardware, and what "good" means.

```photogrid label="1.1" cols="3" ratio="0.9" caption="Three pieces of evidence for software engineering. (a) The page of the Harvard Mark II logbook for 9 September 1947 with the moth taped beside the entry 'First actual case of bug being found'. The word 'bug' for a fault was already in use among engineers, but this page made it famous. (b) Margaret Hamilton beside the printed listing of the Apollo on-board flight software, a stack taller than she is. Her team treated software as an engineered product that needed design, review and testing, and she is credited with promoting the term 'software engineering' in the 1960s. (c) The recovered equipment bay fragment of Ariane 501. The rocket broke up about 37 seconds after lift-off on 4 June 1996 because reused guidance code tried to fit a 64-bit floating point number into a 16-bit signed integer, whose largest value is 32,767. The loss was about 370 million US dollars."
@ photo id="bca252/bug" cap="First 'bug' (1947 logbook)"
fit 0.9
focus 0.5 0.6
call 0.55 0.45 0.4 0.25 "moth taped in"
@ photo id="bca252/hamilton" cap="Apollo software listing"
fit 0.9
focus 0.5 0.45
call 0.8 0.6 0.55 0.85 "printed code"
@ photo id="bca252/ariane" cap="Ariane 501 wreckage"
fit 0.9
focus 0.5 0.5
call 0.5 0.55 0.4 0.2 "recovered fragment"
```

```photogrid label="1.2" cols="2" ratio="1.0" caption="A failure from one wrong unit. (a) NASA's Mars Climate Orbiter during assembly. In September 1999 the spacecraft was lost at Mars because ground software produced thruster impulse data in pound-force seconds while the navigation software expected newton seconds. (b) One pound-force second equals 4.448222 newton seconds, so every number was read about 4.4 times too small. Each team's code was correct on its own; the interface between them was never specified, reviewed or tested."
@ photo id="bca252/mco" cap="Mars Climate Orbiter"
fit 1.0
focus 0.5 0.45
@ svg cap="Same number, different unit"
f = Fig(300, 300)
f.box(10, 20, 130, 60, "Ground\nsoftware", fill=SAND, stroke=AMBER, size=14, bold=True)
f.text(75, 100, "writes 1.00 lbf-s", size=13, color=AMBER, bold=True)
f.box(160, 20, 130, 60, "Navigation\nsoftware", fill=BLUE, stroke=NAVY, size=14, bold=True)
f.text(225, 100, "reads 1.00 N-s", size=13, color=NAVY, bold=True)
f.arrow([(140, 50), (160, 50)], color=RED, sw=2)
f.box(40, 130, 220, 50, "1 lbf-s = 4.448222 N-s", fill=ROSE, stroke=RED, size=14, bold=True)
f.box(40, 195, 220, 50, "error factor 4.448", fill=ROSE, stroke=RED, size=14, bold=True)
f.text(150, 275, "interface never checked", size=13, color=SLATE, bold=True)
```

```svgfig label="1.1" caption="The cost of change rises steeply with the phase in which a fault is found. The ratios 1 : 5 : 10 : 20 : 100 are the commonly quoted pattern from industrial studies (Boehm and others) and are illustrative, not measured on one project. If a wrong requirement costs Rs 500 to correct while it is still on paper, the same fault costs Rs 2,500 at design, Rs 5,000 in coding, Rs 10,000 in testing and Rs 50,000 after release."
f = Fig(580, 250)
names = ["Requirements", "Design", "Coding", "Testing", "After release"]
mult = [1, 5, 10, 20, 100]
base = 500
for i, (n, m) in enumerate(zip(names, mult)):
    h = max(6, 150 * m / 100)
    x = 40 + i * 108
    col = [MINT, MINT, BLUE, SAND, ROSE][i]
    st = [TEAL, TEAL, NAVY, AMBER, RED][i]
    f.box(x, 200 - h, 80, h, "", fill=col, stroke=st)
    f.text(x + 40, 192 - h, "x" + str(m), size=11, color=st, bold=True)
    f.text(x + 40, 216, n, size=10.5, color=SLATE, bold=True)
    f.text(x + 40, 232, "Rs " + format(base * m, ","), size=10.5, color=st, bold=True)
f.text(290, 14, "relative cost to fix the same fault", size=11, color=NAVY, bold=True)
```

```svgfig label="1.2" caption="Hardware and software fail differently. Hardware (dashed) follows a bathtub curve: early failures, a flat useful life, then wear-out. Software (solid) does not wear out, so the useful-life level stays flat, but every change adds a spike of new faults; fixes lower the curve a little each time, yet the level never returns to the original, which is why software is said to deteriorate rather than wear out."
f = Fig(580, 250)
f.line(50, 200, 560, 200, color=SLATE, sw=1.6)
f.line(50, 30, 50, 200, color=SLATE, sw=1.6)
f.text(305, 228, "time", size=10.5, color=SLATE, bold=True)
f.text(8, 20, "failure rate", size=10.5, color=SLATE, bold=True, anchor="start")
import math
hw = []
for i in range(0, 101):
    t = i / 100
    y = 0.30 + 0.9 * math.exp(-t * 14) + 0.9 * math.exp((t - 1) * 9)
    hw.append((50 + t * 500, 200 - min(y, 1.15) * 140))
f.raw('<polyline points="' + " ".join(str(round(a, 1)) + "," + str(round(b, 1)) for a, b in hw) + '" fill="none" stroke="#b45309" stroke-width="2" stroke-dasharray="6 4"/>')
pts = []
level = 0.55
spikes = [0.22, 0.45, 0.68, 0.88]
for i in range(0, 101):
    t = i / 100
    y = 0.95 * math.exp(-t * 12) + level
    for k, s in enumerate(spikes):
        if t >= s:
            y += 0.45 * math.exp(-(t - s) * 40) + 0.04 * (k + 1)
    level2 = 0
    pts.append((50 + t * 500, 200 - min(y, 1.15) * 140 * 0.9))
f.raw('<polyline points="' + " ".join(str(round(a, 1)) + "," + str(round(b, 1)) for a, b in pts) + '" fill="none" stroke="#1d4ed8" stroke-width="2.4"/>')
for s in spikes:
    f.text(50 + s * 500, 42, "change", size=9.5, color=RED, bold=True)
f.text(455, 122, "hardware: wear-out", size=10, color=AMBER, bold=True)
f.text(150, 188, "software: stays above the ideal", size=10, color=NAVY, bold=True)
```

```svgfig label="1.3" caption="What 'good software' means. The four essential attributes (maintainability, dependability and security, efficiency, acceptability) each break into sub-qualities that a team can check in a review. Only the left branch is invisible to the user, which is why it is the first to be sacrificed under deadline pressure."
f = Fig(580, 270)
f.box(215, 8, 150, 40, "Good software", fill=NAVY, stroke=NAVY, color="#ffffff", size=12, bold=True)
cols = [("Maintainability", ["readable code", "modular design", "up-to-date docs"], MINT, TEAL),
        ("Dependability\nand security", ["reliable", "safe", "secure"], ROSE, RED),
        ("Efficiency", ["fast response", "low memory", "low battery"], SAND, AMBER),
        ("Acceptability", ["easy to learn", "compatible", "meets real need"], BLUE, NAVY)]
for i, (t, subs, fl, st) in enumerate(cols):
    x = 10 + i * 144
    f.arrow([(290, 48), (x + 65, 80)], color=SLATE)
    f.box(x, 80, 130, 46, t, fill=fl, stroke=st, size=10.5, bold=True)
    for j, s in enumerate(subs):
        f.box(x + 10, 146 + j * 38, 110, 30, s, fill="#ffffff", stroke=st, size=10, bold=False)
```

### 1.7.1 Eight reasons why software engineering matters in Nepal

1. **Public services depend on software.** Systems such as the Nagarik App, the Department of Transport Management licence records and Tribhuvan University's online result and EMIS portals serve millions of people. When such a system is wrong or down, citizens lose time and money and trust in the service falls. Engineering discipline in requirements, testing and maintenance keeps these systems dependable.
2. **Money moves through code.** ConnectIPS, Fonepay and mobile wallets move real money between banks every second. A single rounding or duplicate-posting fault is multiplied by thousands of transactions, as the Ariane and Mars Climate Orbiter failures show on a larger scale. Testing, code review and audit trails are therefore part of the product, not extras.
3. **Late changes cost far more.** Figure 1.1 shows that the same fault costs about one hundred times more after release than on paper. A Nepali software company that finds a wrong requirement in the first week saves months of rework later. This is the main economic argument for analysis, design review and early testing.
4. **Projects need predictable delivery.** Clients such as banks, ministries and colleges sign contracts with fixed dates and budgets. Estimation, planning and risk management give the team numbers it can defend instead of guesses. Without them, outsourcing firms in Kathmandu either lose money or deliver late.
5. **Software lives for many years.** A billing system written for a hospital in Pokhara may still run ten years later on new hardware and new law. Maintainability, documentation and version control let a new team understand and change it safely. This is why Figure 1.3 puts maintainability first.
6. **Teams, not individuals, build products.** A real product needs analysts, designers, programmers, testers and a client, often in different cities. Common processes, notations such as UML and shared tools let them cooperate without constant misunderstanding. Software engineering supplies that shared language.
7. **Safety and security are at stake.** Software now controls hospital equipment, banking, elections data and the national ID system. A hidden fault or a weakness can harm people or leak private data. Engineering practices such as threat analysis, review and testing reduce the chance and the damage.
8. **Professional ethics build a reputation.** The ACM/IEEE code puts the public interest first, and a company that hides a known fault loses clients quickly in a small market. Honest estimates, honest testing reports and respect for client confidentiality are the basis for long contracts. Ethics is thus both a duty and a business advantage.

## Formula and fact sheet

- Software = programs + data + documentation. Software is engineered, does not wear out, but deteriorates through change.
- Four essential attributes: maintainability, dependability and security, efficiency, acceptability.
- Costs: about 60 % development, 40 % testing; evolution often exceeds development.
- ACM/IEEE code: public first.

## Chapter summary

- Software is more than code, and comes in system, application, embedded, web and AI forms; it can be generic or custom.
- Good software is maintainable, dependable, efficient and acceptable.
- Software engineering is a systematic engineering approach to the whole life cycle; it sits inside the broader field of system engineering.
- Costs are dominated by maintenance and testing; major challenges are heterogeneity, change, security, scale and delivery time.
- Professional practice demands competence, confidentiality and public-interest ethics.

## Practice

1. Define software and explain how it differs from a program.
2. List four types of software with examples.
3. Why is software said to "deteriorate" rather than "wear out"?
4. Name and explain the four essential attributes of good software.
5. Define software engineering and distinguish it from computer science and system engineering.
6. Why does maintenance usually cost more than development?
7. List three key challenges facing software engineering today.
8. State four principles of the ACM/IEEE Code of Ethics with an example breach of one.

::: note Answers and worked solutions
**1.** Software is programs, data structures and documentation. A program is only code written for the author's use; a software product adds documentation, testing, installation support and maintenance for other users.
**2.** System (OS, compiler), application (billing system), embedded (microwave controller), web/mobile (online banking app), AI (a recommender), scientific (simulation).
**3.** Hardware fails from physical wear. Software has no physical wear; but each change can introduce new errors, so the failure rate rises after changes and the software slowly becomes harder to maintain, which is deterioration.
**4.** Maintainability (can evolve), dependability and security (reliable, safe, secure), efficiency (resource use and speed), acceptability (usable and compatible).
**5.** Software engineering: systematic, disciplined, quantifiable approach to developing, operating and maintaining software. Computer science: the theory behind computing. System engineering: whole systems including hardware and people; software engineering is its software part.
**6.** Software needs to change throughout its life: new laws, platforms, features and fixes. Over years of use these changes accumulate and exceed the one-time development effort, particularly for long-lived systems.
**7.** Heterogeneity (many platforms), rapid business change and delivery pressure, and security and trust.
**8.** Public (act in public interest), Client and employer, Product (high standards), Judgment (independent professional judgment). Breach example: hiding a known safety bug from the public to meet a deadline violates the *Public* principle.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the characteristics of software and how they differ from those of hardware.**

*Introduction.* Software is a logical product (programs, data and documentation), so its behaviour differs from that of a physical product (section 1.1 and Figure 1.2).

1. **Software is developed, not manufactured.** The cost lies in design and testing; copying a finished program costs almost nothing, unlike making another physical machine.
2. **Software does not wear out.** Hardware fails from friction, heat and ageing. Software has no such mechanism, so after the early faults are removed the failure rate stays flat (Figure 1.2).
3. **But software deteriorates.** Each change can add new faults, so the curve gets a spike after every release and the baseline slowly rises. Maintenance therefore never restores "as new".
4. **Software is mostly custom-built.** Hardware is assembled from standard chips; most software is still written from scratch, although components and libraries are changing this.
5. **Software is intangible and complex.** A program cannot be seen or weighed, and its behaviour can have many states, so progress is hard to measure.

| Property | Hardware | Software |
|---|---|---|
| Made by | manufacturing | development |
| Failure cause | wear and ageing | design and change faults |
| Failure curve | bathtub | spikes after each change |
| Spare parts | exist | none; faults are fixed in the design |

*Conclusion.* Because software deteriorates through change, controlling change (version control, regression testing) is central to software engineering.

**Q2 (5 marks). Using two real failures, explain why software engineering is needed.**

*Introduction.* Software faults can destroy expensive systems, and both cases in Plates 1.1 and 1.2 came from missing engineering practice, not from missing programming skill.

1. **Ariane 501 (4 June 1996).** The rocket's inertial reference code, reused from Ariane 4, converted a 64-bit floating point value into a 16-bit signed integer. Ariane 5 flew a faster trajectory, the value exceeded 32,767, the conversion raised an exception, and the rocket broke up about 37 seconds after launch with a loss of about 370 million US dollars.
2. **Lesson from Ariane.** Reused components must be re-validated against the new requirements, and the exception handling was never tested with Ariane 5 flight data. Requirements review and realistic testing would have caught it.
3. **Mars Climate Orbiter (1999).** Ground software gave thruster impulse in pound-force seconds while navigation expected newton seconds; since 1 lbf-s = 4.448222 N-s, every value was about 4.4 times too small, and the spacecraft entered the atmosphere of Mars too low.
4. **Lesson from Mars.** The interface between two teams was not formally specified or integration-tested. A written interface specification with units and an end-to-end test would have prevented the loss.
5. **General conclusion.** In both cases each part worked alone and the failure sat in the assumptions between parts. Requirements, interface specification, review and testing are exactly the topics of Units 3 to 6 of this course.

**Q3 (10 marks). Define software engineering. Explain the software crisis, its causes, and how software engineering responds. Discuss the key challenges and the ethical responsibilities of a software engineer.**

*Introduction.* Software engineering is the systematic, disciplined and quantifiable application of engineering principles to the development, operation and maintenance of software. The phrase was chosen at the NATO conference in Garmisch in 1968 in response to the *software crisis*: projects that were late, over budget, unreliable and hard to maintain.

**Symptoms of the crisis.** Projects exceeded schedules and budgets; delivered software did not meet user needs; programs contained many faults; code was so tangled that changes caused new faults; and costs of maintenance grew beyond the cost of development. Figure 1.1 shows why the last two are connected: a fault found after release costs about one hundred times a fault found in requirements.

**Causes.**

1. Hardware power and program size grew faster than the methods for managing complexity.
2. Requirements were vague, incomplete or changing, and nobody wrote them down.
3. Estimates were guesses, so schedules were fiction.
4. Little testing, review or documentation was done.
5. Programmers worked individually, without agreed processes or tools.

**The response.** Software engineering supplies (a) *process models* (Unit 2) that organise the work, (b) *requirements engineering* (Unit 3) that fixes what to build, (c) *design methods* (Unit 4), (d) *coding standards* (Unit 5), (e) *testing and quality assurance* (Unit 6), (f) *maintenance* practice (Unit 7), and (g) *project management* (Unit 8) for estimation, scheduling and risk.

| Crisis symptom | Engineering answer |
|---|---|
| Late and over budget | estimation, scheduling, risk management |
| Wrong product | requirements analysis, prototypes, user review |
| Many faults | reviews, testing, quality assurance |
| Hard to change | modular design, documentation, version control |

**Key challenges today.** Heterogeneity (phones, cloud and legacy systems must work together), rapid business change and pressure for fast delivery, and security and trust, as the Nepali digital payment and e-government systems show.

**Ethics.** The ACM/IEEE code puts the *public* first, then client and employer, product quality, professional judgement, management, profession, colleagues and self. An engineer must not hide a known safety fault, must keep client data confidential, must give honest estimates and must not claim competence they lack.

*Conclusion.* Software engineering turns an unpredictable craft into a managed discipline in which cost, quality and time can be planned; its ethical code makes sure that this power is used for the public good.
