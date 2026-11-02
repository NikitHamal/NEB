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
