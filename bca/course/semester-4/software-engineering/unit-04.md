---
subject: Software Engineering
grade: BCA Semester 4
unit: 4
title: Software Design
hours: 10
area: BCA 252 · Software Engineering · Unit 4
---

Requirements say *what* the system must do; **design** decides *how*. A good design makes code easy to understand, test and change; a bad one makes every change a risk. This unit covers the fundamental design concepts, architectural styles, structured design methods, and user interface design.

::: key What this unit gives you
- Design concepts: abstraction, architecture, patterns, modularity, cohesion and coupling, information hiding, functional independence, refinement.
- Architectural design: repository, client-server, layered models; modular decomposition.
- Procedural design using structured methods; design metrics.
- User interface design: HCI principles, information presentation, interface evaluation; design notation.
:::

## 4.1 Design concepts

| Concept | Meaning |
|---|---|
| **Abstraction** | focus on essentials, suppress detail. *Procedural* abstraction: a named sequence of instructions (`sort()`); *data* abstraction: a named collection of data (a `Student` record); *control* abstraction: a mechanism (loops, iterators) |
| **Architecture** | the overall structure of the software: components, their properties and relationships |
| **Patterns** | a proven solution to a recurring design problem in a context (MVC, Observer, Singleton); the design equivalent of a recipe |
| **Modularity** | dividing the software into separately named and addressable components (modules) that are integrated to satisfy requirements |
| **Information hiding** | each module hides a design decision (its data structure, algorithm) behind a stable interface; changes stay local (Parnas) |
| **Functional independence** | each module has a single, well-defined purpose and little interaction with others; measured by cohesion and coupling |
| **Refinement** | stepwise elaboration (Wirth): start with a statement at a high level of abstraction and decompose it, step by step, into programming-language statements |

**Modularity and cost.** Breaking a problem into modules reduces the cost of understanding each, but increases the cost of *integration*. Total cost is minimised at a moderate number of modules of moderate size; both extreme (one giant module; thousands of tiny ones) are costly.

### Cohesion

**Cohesion** measures how strongly the elements within a module belong together. From best to worst:

| Level | Description | Example |
|---|---|---|
| **Functional** | all elements contribute to one task | `calculate_tax()` |
| **Sequential** | output of one part is input to the next | read → validate → format a record |
| **Communicational** | parts operate on the same data | update and print the same student record |
| **Procedural** | parts follow a sequence of control but are unrelated in data | a routine that opens files, then prints a header |
| **Temporal** | parts are done at the same time | `initialise_everything()` |
| **Logical** | parts do similar things selected by a flag | one `output(type)` function for printer, screen and file |
| **Coincidental** | parts are unrelated | a `misc_utils` module |

### Coupling

**Coupling** measures the interdependence between modules. From loosest (best) to tightest (worst):

| Level | Description |
|---|---|
| **Data** | modules communicate only through simple parameters |
| **Stamp** | they pass a composite structure, of which only part is used |
| **Control** | one passes a flag that controls the logic of the other |
| **External** | both depend on an external format, protocol or device |
| **Common** | both share global data |
| **Content** | one modifies or jumps into the internals of the other |

**Goal: high cohesion, low coupling.** A design with high cohesion and low coupling is easier to understand, test and maintain, since a module can be changed or replaced with minimal effect elsewhere.

::: example Improving a design
Module `report()` takes a `mode` flag (1, 2 or 3) and prints a student, a teacher or a course report using shared global arrays. It has *logical* cohesion and *common/control* coupling. Redesign: three functions `print_student(s)`, `print_teacher(t)`, `print_course(c)` that receive the record they print as a parameter: each has *functional* cohesion and *data* coupling.
:::

## 4.2 Architectural design

The **software architecture** is the structure of the system: major components and how they interact. Early architectural decisions strongly affect performance, security, maintainability and distribution. Common styles (models):

### Repository model

Subsystems exchange data through a central **shared database (repository)**, which they read and write. *Advantages:* efficient sharing of large data; subsystems need not know how others produce data; backup, security and consistency are centralised. *Disadvantages:* all subsystems must agree on one data model (compromises); evolution is hard (data format changes affect everything); the repository is a single point of failure. *Example:* IDEs, CASE tool sets, a hospital database shared by several departments.

### Client-server model

The system is a set of **servers** that provide services (file, print, database, web) and **clients** that use them over a network. *Advantages:* distribution, easy to add servers, services can be replicated. *Disadvantages:* no shared data model so interchange can be inefficient, redundant management in each server, no central registry of names unless one is provided. *Examples:* web applications, e-mail, online banking. **Two-tier**: thin client with presentation on the client and the rest on the server; or **three-tier**: presentation, application logic and data in separate tiers (browser, application server, database).

### Layered model

The system is organised into layers, each providing services to the layer above and using the layer below. *Advantages:* supports incremental development, changes to one layer only affect adjacent ones, replaceable layers. *Disadvantages:* strict layering is hard, and performance suffers when a request passes through many layers. *Examples:* the OSI network model, operating systems, a typical business application: *UI → business logic → data access → database*.

### Model–view–controller (MVC) pattern

Separates the **model** (data and business rules), the **view** (presentation) and the **controller** (input handling). The same data may have many views, and changes in the model update all views. It is the basis of most web frameworks (Laravel, Django, Spring MVC).

### Modular decomposition

A subsystem is further divided into modules. Two strategies: **object-oriented decomposition**, into a set of loosely coupled objects with defined interfaces; and **function-oriented (pipeline) decomposition**, into functional modules that accept input and transform it into output, as in a data-flow pipeline (compiler: lexer → parser → code generator). Pipelines are simple and reusable but need agreed data formats.

### Control models

*Centralised control* (a manager module calls others: call-return, as in structured programs) versus *event-based control* (the system responds to events, as in GUIs and real-time systems).

## 4.3 Procedural design with structured methods

**Structured design** starts from a data-flow diagram (DFD) of the requirements and maps it to a **structure chart**, a hierarchy of modules in which each box is a module and arrows show calls and the data (and control flags) passed between them.

Two mapping strategies:

- **Transform analysis**: for a DFD with clear input, central transformation, and output flows. Identify the *afferent* (input) branches, the central transform, and the *efferent* (output) branches. Create a top-level controller module with branches for each.
- **Transaction analysis**: for a DFD where one input transaction triggers one of several flows; create a *transaction centre* module that reads the transaction type and dispatches to the appropriate module.

**Guidelines:** keep the module span (fan-out) to about 7 ± 2; aim for high fan-in for utility modules (reuse); depth of the hierarchy should be moderate; each module should be a few dozen lines at most.

### Design metrics: fan-in and fan-out

**Fan-in** of a module = number of modules that call it; **fan-out** = number of modules it calls. The **Henry–Kafura** information-flow complexity of a module is

**length × (fan-in × fan-out)²**

where length is the size of the module in lines. A module of 6 lines with fan-in 3 and fan-out 2 scores 6 × (3 × 2)² = **216**; the same size module with fan-in 1 and fan-out 1 scores 6 × 1 = **6**. The squared term means that a module with many connections to others (a design hot-spot) stands out, and tends to correlate with defects and with change effort. Values far above those of the other modules should be redesigned.

### Procedural design notations

Detailed design is expressed with **flowcharts**, **pseudo-code (program design language)**, **structured English**, **decision tables** and **Nassi–Shneiderman diagrams**. Pseudo-code is the most usual: it uses the keywords of structured programming (`IF … THEN … ELSE`, `WHILE`, `FOR`, `CASE`) and informal language for the actions, so it can be read by non-programmers and converted line by line to code.

::: example Pseudo-code for issuing a book
```text
PROCEDURE issue_book(member, copy)
    IF member.card_expired THEN
        REPORT "card expired"; RETURN
    IF count_loans(member) >= 5 THEN
        REPORT "limit reached"; RETURN
    IF copy.reserved_for IS NOT member THEN
        REPORT "reserved"; RETURN
    CREATE loan(member, copy, today + 14 days)
    SET copy.status TO "on loan"
END PROCEDURE
```
:::

## 4.4 User interface design

The user interface (UI) is the part of the system users meet; to them it *is* the system. A poor UI leads to errors and abandonment even when the functions are right.

### Human–computer interaction principles

Design principles (Shneiderman's eight golden rules, Nielsen's heuristics): **consistency** (same actions, same terms), **shortcuts** for experts, **informative feedback**, **closure** (clear end to a sequence), **error prevention and simple error handling**, **easy reversal of actions (undo)**, **user in control**, and **reduced short-term memory load** (recognition over recall; at most 7 ± 2 items). Also **user familiarity** (use the users' concepts, not the computer's), **minimal surprise**, **recoverability**, **user guidance** (help, meaningful error messages) and **user diversity** (accessibility; Nepali Unicode support).

### Interaction styles

| Style | Advantages | Disadvantages | Used for |
|---|---|---|---|
| **Direct manipulation** | quick to learn, immediate feedback | hard to program, screen-space | drag-and-drop, drawing |
| **Menu selection** | little typing, few errors | slow for experienced users | ATMs, forms |
| **Form fill-in** | simple entry, easy to learn | consumes screen space | data entry |
| **Command language** | powerful, flexible | hard to learn, error-prone | experts, scripting |
| **Natural language** | accessible | ambiguous, long | voice assistants, chatbots |

### Information presentation

Separate the information from its presentation (MVC). Choose the form by the type of information: **numeric** data as graphs and bar charts for trends, text for exact values; **colour** used sparingly (about 4 to 5 colours, redundantly coded for colour-blind users, with culturally appropriate meanings); **alerts** distinguishable and consistent; **dynamic** information shown as it changes. Layout should follow a clear visual hierarchy.

### Interface evaluation

Evaluate the interface with users: **usability testing** (observe real users doing tasks, measure time, errors, satisfaction), **heuristic evaluation** (experts check against guidelines), **questionnaires**, **think-aloud sessions**, **video** and logging. Revise and re-test: UI design is iterative, and prototypes are essential. Typical metrics: learning time, task time, error rate, retention, subjective satisfaction. (Semester II's UX/UI Design book treats these in depth.)

## Formula and fact sheet

- Cohesion best → worst: functional, sequential, communicational, procedural, temporal, logical, coincidental.
- Coupling best → worst: data, stamp, control, external, common, content. Aim: **high cohesion, low coupling**.
- Henry–Kafura = length × (fan-in × fan-out)².
- Styles: repository, client-server, layered, MVC, pipeline.
- Transform analysis vs transaction analysis.

## Chapter summary

- Design concepts (abstraction, modularity, information hiding, refinement, functional independence) aim at modules with high cohesion and low coupling.
- Architectural styles organise the system: repository, client-server, layered, MVC; modules are decomposed by objects or functions.
- Structured design maps DFDs to structure charts by transform or transaction analysis, with fan-in/fan-out metrics and pseudo-code for the detail.
- UI design follows HCI principles; the choice of interaction style and presentation depends on users and tasks, and is validated by evaluation.

## Practice

1. Explain abstraction, modularity and information hiding with examples.
2. Rank the types of cohesion and coupling and explain why functional cohesion and data coupling are the best.
3. A function `process(flag)` does validation if flag = 1, saving if flag = 2, and printing if flag = 3. Identify its cohesion and coupling problems and fix them.
4. Compare the repository, client-server and layered models, with one advantage and disadvantage each.
5. What is MVC, and why is it useful for web applications?
6. Distinguish transform analysis and transaction analysis.
7. Compute the Henry–Kafura complexity for a 10-line module with fan-in 2 and fan-out 3.
8. List the HCI principles that apply to an ATM interface.
9. How is a user interface evaluated?

::: note Answers and worked solutions
**1.** Abstraction: use `sort(list)` without knowing the algorithm. Modularity: split a system into `Billing`, `Inventory`, `Reports`. Information hiding: a `Stack` hides whether it uses an array or a linked list; callers use only `push` and `pop`.
**2.** Cohesion: functional > sequential > communicational > procedural > temporal > logical > coincidental. Coupling: data > stamp > control > external > common > content (loosest first). Functional cohesion and data coupling make modules single-purpose and independent, so each can be understood, tested and changed separately.
**3.** Logical cohesion (unrelated tasks chosen by a flag) and control coupling (the caller controls the callee's logic). Fix by splitting into `validate()`, `save()` and `print()`, each with functional cohesion and data coupling.
**4.** Repository: shared data; but single point of failure and one data model. Client-server: distribution and scalability; but redundant management and no shared model. Layered: replaceable layers and incremental development; but performance cost across layers.
**5.** Model–view–controller separates data/rules, presentation and input handling. The UI can change (web, mobile) without changing business rules, and the same data can have several views; teams can work in parallel.
**6.** Transform analysis maps a DFD with distinct input, transform and output streams into a controller with input, process and output branches. Transaction analysis maps a DFD in which one input selects one of many flows into a dispatcher module and one module per transaction type.
**7.** 10 × (2 × 3)² = 10 × 36 = **360**.
**8.** Consistency, informative feedback, error prevention and handling, ability to cancel/reverse, simplicity (menu selection), minimal short-term memory load, accessibility (language, large text), and security cues.
**9.** By usability tests with real users (time, errors, satisfaction), heuristic evaluation by experts, questionnaires, think-aloud sessions and logging; findings feed the next iteration.
:::
