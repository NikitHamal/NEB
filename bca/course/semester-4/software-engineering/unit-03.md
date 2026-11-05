---
subject: Software Engineering
grade: BCA Semester 4
unit: 3
title: Software Requirement Analysis and Specification
hours: 10
area: BCA 252 · Software Engineering · Unit 3
---

The hardest part of building a software system is deciding precisely what to build. No other part so cripples the resulting system if done wrong, and none is more difficult to repair later. A famous tunnel-bore analogy: the cost of fixing a requirements error found in operation can be 50 to 100 times that of fixing it at the requirements stage, according to Boehm's classic studies (the exact multiplier varies by project and has been debated, but the direction is not disputed). This unit teaches how requirements are classified, gathered, analysed, validated, written down and checked for feasibility.

::: key What this unit gives you
- System versus software requirements; user, functional, non-functional and domain requirements.
- Elicitation techniques: interviews, viewpoints, scenarios, use cases, ethnography.
- Validation, the Software Requirements Specification (SRS), and feasibility study.
:::

## 3.1 System and software requirements

A **requirement** is a description of a service the system should provide or a constraint on it. Requirements are written at different levels of detail for different readers:

| Level | Reader | Style |
|---|---|---|
| **User requirements** | clients, managers, end users | natural language, simple tables and diagrams: "The system shall let a librarian issue a book" |
| **System requirements** | engineers, architects, testers | structured, precise, detailed: inputs, outputs, rules, limits |

*Example.* User: "The library system shall remind members of overdue books." System: "1.1 Every day at 06:00 the system shall list loans overdue by one or more days. 1.2 For each, it shall send an SMS to the member's registered number. 1.3 No member shall be sent more than one reminder per day."

## 3.2 Types of software requirements

### Functional requirements

Statements of services the system must provide, how it reacts to inputs and how it behaves in particular situations. Example: "A user shall be able to search the catalogue by title, author or ISBN."

### Non-functional requirements (NFRs)

Constraints on services or the system as a whole: performance, reliability, security, usability, portability, standards. They often matter more than functional ones; a system that does everything but is too slow or unsafe is useless. Three classes:

| Class | Examples |
|---|---|
| **Product** requirements | speed (response < 2 s for 95 % of searches), reliability (availability 99.5 %), usability (a new user learns the basics in 30 minutes), portability |
| **Organisational** requirements | development process, standards (ISO), delivery dates, implementation language |
| **External** requirements | legal (privacy law), ethical, interoperability with other systems, regulations |

**Writing NFRs testably.** "The system shall be easy to use" is a *goal*; "Trained staff shall be able to issue a book in under 20 seconds and make fewer than 2 errors per 100 transactions" is a *verifiable requirement*. Metrics: speed (transactions per second, response time), size (MB), ease of use (training time, error rate), reliability (mean time to failure, availability), robustness (restart time), portability (number of target systems).

### Domain requirements

Come from the application domain and reflect its characteristics: a train-control system must respect braking rules from the railway's regulations; a banking system must follow interest calculation rules. If the developers do not know the domain they will miss implicit requirements, so domain experts take part.

## 3.3 Requirements engineering process

The process has four activities, repeated in a spiral: **feasibility study**, **elicitation and analysis**, **specification**, and **validation**; **requirements management** runs through all of them, tracking changes.

## 3.4 Elicitation and analysis

Elicitation is hard: stakeholders do not know what they want, express it in their own terms, conflict with each other, and requirements change during analysis (because the business changes). The stages: discovery, classification and organisation, prioritisation and negotiation, and documentation.

### Viewpoints

Each **stakeholder** (a person or system with an interest) sees the system differently. **Viewpoint-oriented** approaches organise requirements around them: *interactor* viewpoints (people and systems that interact, such as librarians, members), *indirect* viewpoints (those who influence requirements without interacting, such as the management and regulators), and *domain* viewpoints (domain constraints). For a university result system: students, teachers, examination controller, IT staff, the Dean's office.

### Interviewing

**Closed** interviews use a predefined list of questions; **open** interviews explore issues freely. Real interviews mix them. Good practice: be open-minded, prompt with a prototype or a starting question, and remember that interviewees use domain jargon and omit what is obvious to them. Interviews are poor for discovering domain constraints and organisational politics.

### Scenarios

Scenarios are real-life examples of how the system might be used. Each includes: the situation before, the normal flow of events, what can go wrong and how it is handled, other concurrent activity, and the state after.

::: example Scenario: issuing a book
*Initial assumption:* the librarian is logged in and the member has presented a card. *Normal:* the librarian scans the card; the system displays the member's name and loans; the librarian scans the book; the system records the loan and due date (14 days) and prints a slip. *What can go wrong:* the card is expired (system refuses and shows the message), the member has five loans already (refuses), the book is reserved for another member (warns). *Other activity:* another terminal may be searching the catalogue. *End state:* the book is marked on loan.
:::

### Use cases

A **use case** describes an interaction between an **actor** (a person or external system) and the system to achieve a goal. A **use-case diagram** shows actors (stick figures), use cases (ovals) and the system boundary (a rectangle); relationships: **association** (actor takes part), **include** (a use case always invokes another, such as "Issue book" includes "Verify membership") and **extend** (optional behaviour, such as "Pay fine" extending "Return book").

A structured text use case:

| Field | Content |
|---|---|
| Name | Issue book |
| Actor | Librarian (primary), Member |
| Precondition | Librarian authenticated; member card valid |
| Main flow | 1. Scan card. 2. System displays member. 3. Scan book. 4. System records loan and due date. 5. System prints slip. |
| Alternative flows | 2a. Card expired → show message, end. 3a. Limit exceeded → refuse. 3b. Book reserved → warn, ask to confirm. |
| Postcondition | Loan recorded; copy status = On loan |

Use cases and scenarios give the *functional* requirements as seen by users; they are effective for discovery but weak at expressing non-functional and domain requirements.

### Ethnography

An analyst *observes* how people really work, spending time in the workplace. Because people often cannot articulate their tacit knowledge or how they cope with exceptions, ethnography reveals real processes, cooperation and social constraints, such as informal workarounds in a hospital ward or a bank counter. It needs time and does not reveal new features that the system could offer, so it is combined with other techniques.

### Other techniques

Questionnaires (wide reach, shallow), workshops/JAD sessions (conflicts solved in the room), prototyping (users react to something concrete), document analysis (existing forms and reports), and brainstorming.

### Prioritisation and negotiation

Stakeholders disagree, so requirements are prioritised, often by **MoSCoW** (Must, Should, Could, Won't) or by value and cost; conflicts are negotiated with explicit trade-offs and agreed ownership.

## 3.5 Requirements validation

Check that the requirements define the system the customer really wants. Errors found here are far cheaper than later. Checks:

- **Validity**: does the system provide the functions that best support the users?
- **Consistency**: no conflicting requirements.
- **Completeness**: all functions and constraints included.
- **Realism**: implementable with the technology and budget available.
- **Verifiability**: testable; can the final system be shown to meet it?

Techniques: **requirements reviews** (systematic manual analysis by a team of client and developer staff, with a checklist), **prototyping** (let users try a model), **test-case generation** (if a test cannot be written the requirement is probably vague).

**Requirements change** is unavoidable: management must keep traceability (links from each requirement to its source, design and tests), control change through a formal request, impact analysis and approval, and baseline each version.

## 3.6 Software requirements specification (SRS)

The **SRS** is the official statement of what the developers must implement. Readers: customers (to check), managers (to plan), engineers (to build), testers (to validate), maintainers. The IEEE 830 structure:

1. **Introduction**: purpose, scope, definitions and acronyms, references, overview.
2. **Overall description**: product perspective, product functions (summary), user characteristics, constraints, assumptions and dependencies.
3. **Specific requirements**: external interface requirements (user, hardware, software, communication), functional requirements (organised by feature, use case or class), performance requirements, design constraints, quality attributes (reliability, availability, security, maintainability), other requirements.
4. **Appendices and index.**

**Characteristics of a good SRS** (IEEE 830): *correct*, *unambiguous*, *complete*, *consistent*, *ranked for importance*, *verifiable*, *modifiable*, *traceable*. Natural-language ambiguity is the big problem, so structured aids help: structured natural language with standard forms, **tables** and **decision tables**, **pseudo-code** (program design language), **graphical models** (DFD, use cases, state diagrams), and mathematical (formal) specifications for safety-critical systems.

::: example Spotting a bad requirement
"The system shall respond quickly and be user friendly" fails the test: *quickly* and *friendly* are unverifiable. Rewrite: "The system shall display search results within 2 seconds for 95 % of queries with up to 10 concurrent users. 90 % of first-time librarians shall complete an issue transaction without help after a 30-minute training session."
:::

## 3.7 Feasibility study

Before major effort is invested, ask: *is the project worth doing, and can it be done?* A feasibility report answers whether the system:

| Type | Question |
|---|---|
| **Technical** | can it be built with available technology and skills? |
| **Economic** | do the benefits exceed costs (cost-benefit analysis, payback)? |
| **Operational** | will it be used by the people and fit the organisation? |
| **Schedule** | can it be delivered in the time available? |
| **Legal** | does it comply with law and contracts? |

The feasibility study is short (a few weeks) and ends with a *go / no-go* recommendation, with alternatives (do nothing, buy, build, outsource) and their costs. Estimates from Unit 8 (COCOMO, function points) feed the cost side.

## 3.8 Requirements in pictures: a lesson from the year 2000

A requirement that is never written down is a requirement that is never tested. Plate 3.1 shows the best-known example: the year-2000 problem. The Figures 3.1 to 3.6 then draw the requirements engineering process, a use case diagram, testable quality requirements, prioritisation, the layout of an SRS and a feasibility calculation.

```photogrid label="3.1" cols="3" ratio="1.0" caption="The year-2000 problem as a requirements failure. (a) A 'Y2K compliant, millennium-proof' sticker of the kind attached to computers in 1999, with the date of testing written in by hand. (b) An 80-column punched card: each column was costly, so designers stored the year in two digits and nobody wrote the requirement 'dates shall work after 1999'. Programs written in the 1960s and 1970s were still running in 1999. (c) What goes wrong with two-digit years: the age of a person born in 1985, computed on 31 December 1999 and on 1 January 2000, falls from 14 to a negative number."
@ photo id="bca252/y2k" cap="Y2K compliance sticker"
fit 1.0
focus 0.5 0.5
@ photo id="bca252/card" cap="80-column punched card"
fit 1.0
focus 0.4 0.5
@ svg cap="Two-digit year arithmetic"
f = Fig(300, 300)
f.box(10, 14, 280, 40, "age = current year - birth year", fill=BLUE, stroke=NAVY, size=13, bold=True)
f.box(10, 70, 280, 50, "31 Dec 1999: 99 - 85 = 14", fill=MINT, stroke=TEAL, size=14, bold=True)
f.box(10, 136, 280, 50, "1 Jan 2000: 00 - 85 = -85", fill=ROSE, stroke=RED, size=14, bold=True)
f.text(150, 214, "missing requirement:", size=13, color=SLATE, bold=True)
f.text(150, 236, "four-digit years", size=13, color=RED, bold=True)
f.text(150, 262, "never specified, never tested", size=13, color=SLATE, bold=True)
```

```svgfig label="3.1" caption="The requirements engineering process. A feasibility study decides whether to go on; elicitation and analysis discover the requirements; specification writes them down as the SRS; validation checks the SRS with the users. Requirements management runs alongside all of them because requirements keep changing. Each arrow back shows rework that is cheap now and expensive later (Figure 1.1)."
f = Fig(580, 230)
steps = [("Feasibility\nstudy", BLUE, NAVY), ("Elicitation and\nanalysis", MINT, TEAL), ("Specification\n(SRS)", SAND, AMBER), ("Validation", ROSE, RED)]
for i, (t, fl, st) in enumerate(steps):
    x = 10 + i * 144
    f.box(x, 40, 120, 56, t, fill=fl, stroke=st, size=10.5, bold=True)
    if i < 3:
        f.arrow([(x + 120, 68), (x + 144, 68)], color=SLATE)
f.arrow([(502, 96), (502, 130), (190, 130), (190, 96)], color=RED, dash=True)
f.text(346, 124, "errors found: go back and revise", size=9.5, color=RED, bold=True)
f.box(10, 160, 560, 40, "Requirements management: track changes, versions, traceability to design and tests", fill="#ffffff", stroke=SLATE, size=10.5, bold=True)
f.text(70, 20, "feasibility report", size=9.5, color=SLATE)
f.text(502, 20, "validated SRS", size=9.5, color=SLATE)
```

```svgfig label="3.2" caption="A use case diagram for a college result system. The rectangle is the system boundary; the three actors (Student, Examiner, Administrator) are outside it; each oval is one use case, a goal an actor can achieve. The dashed include arrow means that viewing a result always runs the login use case first."
f = Fig(580, 270)
f.box(150, 8, 300, 254, "", fill="#ffffff", stroke=SLATE, sw=1.5)
f.text(300, 26, "Result processing system", size=11, color=NAVY, bold=True)
def actor(x, y, name):
    f.circle(x, y, 9, fill="#ffffff", stroke=NAVY)
    f.line(x, y + 9, x, y + 38, color=NAVY, sw=1.6)
    f.line(x - 14, y + 20, x + 14, y + 20, color=NAVY, sw=1.6)
    f.line(x, y + 38, x - 12, y + 58, color=NAVY, sw=1.6)
    f.line(x, y + 38, x + 12, y + 58, color=NAVY, sw=1.6)
    f.text(x, y + 74, name, size=10.5, color=NAVY, bold=True)
actor(60, 40, "Student")
actor(60, 170, "Examiner")
actor(520, 105, "Administrator")
ucs = [(300, 56, "View result"), (300, 106, "Log in"), (230, 158, "Enter marks"), (370, 158, "Publish results"), (300, 214, "Manage users")]
for x, y, t in ucs:
    f.raw('<ellipse cx="' + str(x) + '" cy="' + str(y) + '" rx="62" ry="22" fill="#e0f2fe" stroke="#1e3a8a" stroke-width="1.4"/>')
    f.text(x, y + 1, t, size=10, color=NAVY, bold=True, vmid=True)
f.line(74, 70, 238, 56, color=SLATE)
f.line(74, 190, 172, 160, color=SLATE)
f.line(506, 120, 420, 156, color=SLATE)
f.line(506, 130, 350, 208, color=SLATE)
f.arrow([(300, 78), (300, 84)], color=AMBER, dash=True)
f.text(352, 86, "include", size=9.5, color=AMBER, bold=True)
```

```svgfig label="3.3" caption="From vague to testable. A non-functional requirement that cannot be measured cannot be verified, so each vague wish on the left is rewritten as a number with a condition on the right. The test column says how the requirement would be checked."
f = Fig(580, 250)
rows = [("The system shall be\nfast", "95% of result queries answer\nwithin 2 s with 500 users", "load test"),
        ("The system shall be\nreliable", "availability of at least\n99.5% per month", "uptime log"),
        ("The system shall be\nsecure", "passwords stored hashed;\n5 failed logins lock account", "security test"),
        ("The system shall be\neasy to use", "a trained clerk enters 10 marks\nin under 3 minutes", "usability trial")]
f.text(105, 16, "Vague", size=11, color=RED, bold=True)
f.text(350, 16, "Measurable requirement", size=11, color=TEAL, bold=True)
f.text(536, 16, "Test", size=11, color=NAVY, bold=True)
for i, (a, b, c) in enumerate(rows):
    y = 28 + i * 54
    f.box(8, y, 190, 40, a, fill=ROSE, stroke=RED, size=9.5, bold=True)
    f.arrow([(198, y + 20), (216, y + 20)], color=SLATE)
    f.box(216, y, 250, 40, b, fill=MINT, stroke=TEAL, size=9.5, bold=True)
    f.box(476, y, 96, 40, c, fill=BLUE, stroke=NAVY, size=9.5, bold=True)
```

```svgfig label="3.4" caption="Prioritising requirements by value for effort. Each requirement gets a business value (1 to 10) and a cost (person-days); the ratio value / cost ranks the list. The backup requirement (8 / 2 = 4.0) comes first and the dark theme (2 / 4 = 0.5) last, so if time runs out the least valuable item is dropped."
f = Fig(580, 250)
items = [("Daily backup", 8, 2), ("SMS alerts", 6, 2), ("Print transcript", 7, 3), ("Online fee payment", 9, 5), ("Attendance report", 5, 5), ("Dark theme", 2, 4)]
items.sort(key=lambda r: -r[1] / r[2])
f.text(290, 14, "value / cost", size=11, color=NAVY, bold=True)
for i, (n, v, c) in enumerate(items):
    y = 28 + i * 36
    r = v / c
    f.text(150, y + 16, n, size=10.5, color=SLATE, bold=True, anchor="end")
    f.box(160, y + 2, r * 70, 24, "", fill=[MINT, MINT, MINT, BLUE, SAND, ROSE][i], stroke=[TEAL, TEAL, TEAL, NAVY, AMBER, RED][i])
    f.text(160 + r * 70 + 8, y + 16, format(r, ".2f") + "   (" + str(v) + " / " + str(c) + ")", size=10, color=SLATE, bold=True, anchor="start")
f.text(290, 246, "build from the top of the list down", size=10, color=SLATE)
```

```svgfig label="3.5" caption="The layout of an SRS following the IEEE 830 pattern. Section 1 says why the document exists, section 2 describes the product in general, section 3 holds the numbered, testable requirements (the part programmers and testers use every day), and the appendices keep supporting material."
f = Fig(580, 270)
f.box(10, 8, 270, 254, "", fill="#ffffff", stroke=SLATE, sw=1.5)
blocks = [("1 Introduction", "purpose, scope, definitions", BLUE, NAVY),
          ("2 Overall description", "product, users, constraints", MINT, TEAL),
          ("3 Specific requirements", "functions, interfaces, performance", SAND, AMBER),
          ("4 Appendices and index", "samples, models, change history", ROSE, RED)]
for i, (t, d, fl, st) in enumerate(blocks):
    y = 18 + i * 60
    f.box(20, y, 250, 52, t, fill=fl, stroke=st, size=10.5, bold=True)
    f.text(145, y + 40, d, size=8.5, color=SLATE)
f.box(310, 20, 260, 50, "REQ-3.2.1 The system shall let\nan examiner enter marks 0 to 100.", fill="#ffffff", stroke=TEAL, size=9, bold=True)
f.box(310, 84, 260, 50, "REQ-3.2.2 The system shall reject\na mark above 100 with a message.", fill="#ffffff", stroke=TEAL, size=9, bold=True)
f.box(310, 148, 260, 50, "REQ-3.4.1 A result page shall\nload in 2 s for 95% of requests.", fill="#ffffff", stroke=TEAL, size=9, bold=True)
f.text(440, 218, "numbered, atomic, testable", size=10.5, color=TEAL, bold=True)
f.text(440, 238, "each id is traced to a test", size=10, color=SLATE)
f.arrow([(270, 138), (310, 110)], color=AMBER, sw=1.8)
```

```svgfig label="3.6" caption="A feasibility check in numbers. A result system costs Rs 12,00,000 to build and saves Rs 5,00,000 a year. Cumulative net benefit is negative for the first two years and positive in year 3; the payback period is 12,00,000 / 5,00,000 = 2.4 years. Over five years the benefit is 25,00,000, net gain 13,00,000, a return of 13,00,000 / 12,00,000 = 108.3%."
f = Fig(580, 250)
f.line(60, 150, 560, 150, color=SLATE, sw=1.5)
f.line(60, 20, 60, 230, color=SLATE, sw=1.5)
vals = [-12 + 5 * y for y in range(0, 6)]
for y, v in enumerate(vals):
    x = 90 + y * 82
    h = abs(v) * 8
    if v < 0:
        f.box(x, 150, 50, h, "", fill=ROSE, stroke=RED)
        f.text(x + 25, 150 + h + 14, "-" + str(abs(v)) + " lakh", size=10, color=RED, bold=True)
    else:
        f.box(x, 150 - h, 50, h, "", fill=MINT, stroke=TEAL)
        f.text(x + 25, 150 - h - 6, "+" + str(v) + " lakh", size=10, color=TEAL, bold=True)
    f.text(x + 25, 244, "year " + str(y), size=10, color=SLATE, bold=True)
f.text(380, 30, "payback = 12 / 5 = 2.4 years", size=11, color=NAVY, bold=True)
```

### 3.8.1 Eight characteristics of a good SRS

1. **Correct.** Every requirement stated is something the system must really do, as confirmed by the customer. A wrong requirement, such as a wrong grading rule for a University result system, is built faithfully and produces wrong results. Review with the users is the only way to check correctness.
2. **Unambiguous.** Each requirement can be read in only one way by customer, designer and tester. Words such as "fast", "user-friendly" and "etc." are replaced by measurable statements, as in Figure 3.3. Ambiguity is the main source of disputes between a client and a software company.
3. **Complete.** All functions, inputs, outputs, interfaces and quality needs are included, and every response to every input is defined. Gaps are costly, because the programmers fill them with their own guesses. The year-2000 case in Plate 3.1 is a gap that survived for thirty years.
4. **Consistent.** No two requirements contradict each other and the same term always means the same thing. If one section says marks are out of 100 and another says out of 50, the design cannot satisfy both. A glossary and a careful review catch these conflicts.
5. **Ranked for importance and stability.** Each requirement is marked essential, desirable or optional, and by how likely it is to change. This lets the team build the important and stable parts first, as in Figure 3.4. It also tells the client what can be cut when money or time is short.
6. **Verifiable.** There is a finite, cost-effective way to check that the finished product meets each requirement, such as a test, an inspection or a demonstration. "The system shall be reliable" fails this test; "99.5 per cent availability per month" passes it. Unverifiable requirements cannot be accepted or rejected.
7. **Modifiable.** The structure is organised so that a change touches only one place, with no repetition of the same fact. Requirements change constantly, for example when a fee rule changes, so the document must be easy to update. Numbered requirements and a good table of contents help.
8. **Traceable.** Every requirement has a unique number, and each can be followed forward to design, code and tests and backward to its source. When a requirement changes, the team can find everything that is affected. Traceability is also how an auditor or a client checks that nothing was left out.

## Formula and fact sheet

- User requirements (natural language, for clients) versus system requirements (detailed, for developers).
- Functional / non-functional (product, organisational, external) / domain requirements. NFRs must be verifiable with a metric.
- Elicitation: viewpoints, interviews, scenarios, use cases (include, extend), ethnography.
- Validation checks: validity, consistency, completeness, realism, verifiability.
- SRS qualities: correct, unambiguous, complete, consistent, ranked, verifiable, modifiable, traceable.

## Chapter summary

- Requirements are written at user and system levels and divided into functional, non-functional and domain requirements.
- Elicitation uses viewpoints, interviews, scenarios, use cases and ethnography, followed by prioritisation and negotiation.
- Validation uses reviews, prototypes and test-case writing to catch errors early.
- The SRS records the agreed requirements in a standard structure; the feasibility study decides whether to proceed.

## Practice

1. Differentiate user and system requirements with an example.
2. Distinguish functional, non-functional and domain requirements, with an example of each for a hospital system.
3. Rewrite "The system should be fast and easy to use" as verifiable requirements.
4. Describe three elicitation techniques and a weakness of each.
5. Draw (describe) a use case diagram for an online ticket booking system, including one include and one extend relationship.
6. List five checks used in requirements validation.
7. Outline the structure of an SRS and list four qualities of a good SRS.
8. What is a feasibility study and which types of feasibility are considered?
9. Why is it said that errors in requirements are the most expensive?

::: note Answers and worked solutions
**1.** User: "The system shall let patients book appointments online" (natural language for clients). System: "Booking shall accept doctor, date and slot; refuse a slot already booked; send a confirmation SMS within 60 seconds" (detailed, for developers).
**2.** Functional: "The doctor can view a patient's history." Non-functional: "Search results appear within 3 seconds; 99.9 % availability; compliant with patient-privacy law." Domain: "Drug dosage calculations shall follow the hospital's clinical protocol."
**3.** "95 % of page loads shall complete in under 2 seconds with 50 concurrent users. A first-time user shall be able to complete a booking within 3 minutes, without help, in at least 90 % of trials."
**4.** Interviews (rich detail; miss tacit knowledge and politics); scenarios (concrete; poor for non-functional needs); ethnography (shows real work; slow, finds no new ideas); use cases (clear goals; weak for domain constraints).
**5.** Actors: Customer, Payment Gateway, Admin. Use cases: Search tickets, Book ticket, Pay, Cancel booking. "Book ticket" «include» "Pay"; "Cancel booking" «extend» "Issue refund" (optional, if the ticket is refundable).
**6.** Validity, consistency, completeness, realism, verifiability (and traceability).
**7.** Introduction; overall description; specific requirements (interfaces, functions, performance, constraints, quality attributes); appendices. Qualities: correct, unambiguous, complete, consistent, verifiable, modifiable, traceable, ranked.
**8.** A short study at the start of a project to decide whether it is worth doing and possible. Technical, economic, operational, schedule and legal feasibility.
**9.** Requirements are the basis for all later work. A mistake propagates into design, code and tests; correcting it late means redoing all of them and often rebuilding trust with the customer, so the cost multiplies by the phase.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Differentiate between functional and non-functional requirements with examples for a college result system.**

*Introduction.* Functional requirements say *what* the system must do; non-functional requirements (NFRs) say *how well* it must do it or under what constraints (section 3.2).

1. **Functional requirements** describe services, inputs, outputs and behaviour. Examples: the examiner shall enter marks from 0 to 100; the system shall calculate the GPA from the marks; the student shall view a result by entering a roll number.
2. **Non-functional requirements** describe quality and constraints: performance, reliability, security, usability, portability and legal rules. Example: a result page shall load within 2 seconds for 95% of requests with 500 users.
3. **Testing.** A functional requirement is tested by checking a result for given inputs; an NFR is tested by measurement (load test, uptime log), as in Figure 3.3.
4. **Importance.** A system that fails a functional requirement does not work; a system that fails an NFR works badly or unsafely, and NFRs often decide the architecture.

| Aspect | Functional | Non-functional |
|---|---|---|
| Describes | services and behaviour | qualities and constraints |
| Example | calculate GPA | 99.5% availability |
| Verified by | functional test | measurement |
| Failure means | feature missing | poor quality |

*Conclusion.* Both kinds belong in the SRS; vague NFRs must be rewritten as numbers.

**Q2 (5 marks). Explain any four requirements elicitation techniques.**

*Introduction.* Elicitation is discovering what stakeholders need; no single technique is enough, so analysts combine several (section 3.4).

1. **Interviews.** The analyst asks closed and open questions of stakeholders, such as examination officers. They give detailed knowledge but depend on the person's memory and honesty.
2. **Scenarios and use cases.** A typical use is described step by step, such as "Examiner enters marks" (Figure 3.2). Scenarios make requirements concrete and expose missing steps.
3. **Questionnaires and surveys.** Many users answer fixed questions, which is cheap for large groups such as all students, but the answers are shallow and cannot be followed up.
4. **Observation (ethnography).** The analyst watches people work in their real setting, for example the clerk at the admission counter. This reveals tacit knowledge that people forget to mention, and shows workarounds and problems.
5. **Prototyping and workshops** (extra). A mock-up screen makes users react, and a joint workshop resolves conflicting viewpoints quickly.

*Conclusion.* Interviews give depth, questionnaires give breadth, observation gives truth and prototypes give feedback.

**Q3 (10 marks). Explain the requirements engineering process with a diagram. Describe feasibility study, elicitation, specification, validation and management.**

*Introduction.* Requirements engineering (RE) is the process of finding out, analysing, documenting and checking the services a system must provide and the constraints on it. It is the foundation of the project, because Figure 1.1 shows that a requirement fault found after release costs about one hundred times more than one found on paper.

**Process (Figure 3.1).**
1. **Feasibility study.** A short study decides whether the system is technically possible, economically worthwhile and operationally acceptable. In Figure 3.6 the project pays back in 2.4 years with a five-year return of 108.3%, so it is feasible. The output is a feasibility report.
2. **Elicitation and analysis.** The analyst finds requirements from stakeholders using interviews, scenarios, use cases, observation and prototypes (Q2), then classifies them, finds conflicts, and negotiates and ranks them (Figure 3.4). Viewpoints, such as students, examiners and administrators, are listed so that nobody is missed.
3. **Specification.** The agreed requirements are written as the software requirements specification (SRS) in a standard layout (Figure 3.5), using natural language, tables and models. Each requirement is numbered, atomic and testable.
4. **Validation.** The SRS is checked for validity, consistency, completeness, realism and verifiability by reviews, prototypes and by writing test cases from the requirements. Errors send the team back, as the dashed arrow shows.
5. **Requirements management.** Requirements change during the project, so changes are controlled: each change is logged, its impact is assessed using the trace links, and it is approved before being built.

| Activity | Input | Output |
|---|---|---|
| Feasibility | idea, budget | feasibility report |
| Elicitation | stakeholders | requirement lists, models |
| Specification | agreed lists | SRS |
| Validation | SRS | validated SRS, test cases |
| Management | change requests | controlled versions |

**Problems.** Stakeholders do not know what they want, express needs in their own terms, conflict with each other, and the environment changes. The process therefore must be iterative.

*Conclusion.* A systematic RE process produces a validated, traceable SRS; it is the cheapest place to remove faults, and the Y2K case in Plate 3.1 shows what an unwritten requirement costs.

**Q4 (10 marks). What is an SRS? Describe its structure and the characteristics of a good SRS. Draw a use case diagram for a college result system.**

*Introduction.* A software requirements specification (SRS) is the official statement of what the developers must build. It is the contract between customer and developer, the basis for design and testing, and the reference for later maintenance.

**Structure (IEEE 830, Figure 3.5).** Section 1 *Introduction*: purpose, scope, definitions, references and overview. Section 2 *Overall description*: product perspective, functions, user classes, operating environment, constraints, assumptions. Section 3 *Specific requirements*: external interfaces, functional requirements, performance, design constraints and quality attributes, each as a numbered statement such as "REQ-3.2.2 The system shall reject a mark above 100". Section 4 *Appendices and index*.

**Characteristics (section 3.8.1).** Correct, unambiguous, complete, consistent, ranked for importance and stability, verifiable, modifiable and traceable. An ambiguous requirement such as "fast response" is replaced by "95% of result queries return within 2 seconds".

**Use case diagram (Figure 3.2).** Actors: Student, Examiner, Administrator. Use cases: View result (includes Log in), Enter marks, Publish results, Manage users. The student is linked to *View result*; the examiner to *Enter marks*; the administrator to *Publish results* and *Manage users*. The system boundary is drawn as a rectangle around the use cases.

**One use case, in detail.** *Enter marks.* Precondition: examiner is logged in. Main flow: choose subject and batch; enter marks; system validates 0 to 100; examiner saves. Alternative: invalid mark, message shown, entry repeated. Postcondition: marks stored.

| Characteristic | Test question |
|---|---|
| Unambiguous | can it be read two ways? |
| Complete | is every input case covered? |
| Verifiable | which test checks it? |
| Traceable | which design item and test does it map to? |

*Conclusion.* A good SRS reduces rework, prevents disputes and is the single document from which design, coding and testing start.
