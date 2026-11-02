---
subject: System Analysis and Design
grade: BCA Semester 3
unit: 3
title: Analysis
hours: 13
area: BCA 204 · System Analysis and Design · Unit 3
---

**Analysis** discovers what the system must do. The analyst gathers **requirements** from the people who will use it, then models the **processes** (data flow diagrams, decision tables) and the **data** (entity-relationship diagrams) in a form users and designers can both check.

::: key What this unit gives you
- Requirements determination: traditional, contemporary and radical methods; agile requirements.
- Process modelling with data flow diagrams, and logic modelling with decision tables.
- Conceptual data modelling with E-R diagrams, supertypes/subtypes, business rules and database patterns.
:::

## 3.1 System requirements and how to determine them

A **requirement** is a statement of what the system must do (**functional**: "the system shall print an admit card") or how well (**non-functional**: performance, security, usability, reliability, legal). Good requirements are **clear, complete, consistent, testable and traceable**; errors found here are the cheapest to fix. Typical analyst activities: collect information, build prototypes, ask "what is the best way to do it?", and gather the **current system's** and the **needed system's** requirements.

### Traditional methods

| Method | Description | Strengths | Weaknesses |
|---|---|---|---|
| **Interviews** | one-to-one structured or open questions | rich detail, can probe | time-consuming, depends on interviewee |
| **Questionnaires** | written questions to many people | wide reach, cheap | low response, no follow-up |
| **Direct observation** | watch work being done | reveals real practice | people behave differently; time |
| **Document analysis** | study forms, reports, manuals, policies | shows formal rules | may be out of date |

Interview tips: prepare questions, begin with open ones, listen, keep notes, confirm understanding, thank the person. Question types: open ("How do you handle returns?") and closed ("Do you print receipts?"); a **questionnaire** should pilot-test its wording and avoid leading questions.

### Contemporary methods

**Joint Application Design (JAD):** a structured workshop of users, managers and analysts (led by a facilitator) that agrees on requirements in days instead of weeks of interviews, with a scribe and CASE tools. **Prototyping:** build a quick working model so users react to something real; good for unclear requirements. **CASE/repository tools** keep requirements in one place. Also **group support systems** and **use cases** (Unit 1).

### Radical methods

**Business Process Reengineering (BPR):** rethink and redesign processes radically for dramatic gains (cost, speed) instead of automating what exists. Steps: identify processes to change, identify **disruptive technologies** (databases, networks, automatic identification), and redesign. Example: replacing a paper approval chain with a single online application. **Process modelling** and **benchmarking** support it, but BPR carries high risk and often meets resistance.

### Requirements management and agile requirements

**Requirements management tools** (Jira, Azure DevOps, Doors) record each requirement with a unique ID, owner, priority, status, source and links to design and tests (**traceability**), and manage **changes** (scope creep). In **agile** projects requirements are **user stories** ("As a *student* I want to *download my admit card* so that *I can sit the exam*") with **acceptance criteria**, kept in a prioritised **product backlog** and refined every sprint; the customer is part of the team, and a "definition of done" says when a story is finished.

## 3.2 Process modelling: data flow diagrams

A **data flow diagram (DFD)** shows how data moves through a system: where it comes from, which **processes** transform it, where it is stored, and where it goes. It shows *what* happens, not *when* or *how* (that is flowcharts and design).

| Element | Yourdon/DeMarco symbol | Gane–Sarson symbol | Rule |
|---|---|---|---|
| **External entity** (source/sink) | rectangle | rectangle | outside the system boundary; names a person/organisation |
| **Process** | circle | rounded rectangle | has at least one input and one output; name = verb phrase ("Verify payment"); numbered |
| **Data store** | two parallel lines | open-ended rectangle | holds data at rest (a file, table); named by contents |
| **Data flow** | arrow | arrow | labelled with the data it carries (a noun) |

### Rules of DFD construction

- No process may have only outputs (**miracle**) or only inputs (**black hole**).
- Data cannot flow directly between two external entities, between two data stores, or between an entity and a store: a **process** must be in between.
- Data flow labels are nouns; process labels are verb phrases; every flow name is unique.
- A flow from a store to a process is a **read**; process to store is a **write**.

### Levels and decomposition

The **context diagram** shows the entire system as one process with its external entities and flows. **Level-0** (the *top-level* DFD) breaks the system into 3–9 major processes with data stores. Each process may then be **decomposed** into a child DFD (level 1: processes 1.1, 1.2 …). **Balancing:** the inputs and outputs of a parent process must exactly match those of its child diagram.

::: example Worked example: college fee system
**Context diagram.** One process **0 College Fee System**. External entities: **Student** and **Bank**. Flows: Student → system: *Admission form*, *Fee payment*; system → Student: *Fee receipt*, *Dues notice*; system → Bank: *Deposit slip*; Bank → system: *Deposit confirmation*.
**Level 0.**

- **1.0 Record admission:** input *Admission form* (Student); writes *Student record* to store **D1 Students**.
- **2.0 Collect fee:** inputs *Fee payment* (Student) and *Fee structure* (from **D3 Fee structure**); output *Fee receipt* to Student; writes *Payment record* to **D2 Payments**; sends *Deposit slip* to Bank.
- **3.0 Confirm deposit:** input *Deposit confirmation* (Bank); updates **D2 Payments**.
- **4.0 Generate dues:** reads **D1 Students** and **D2 Payments**; outputs *Dues notice* to Student.
**Balancing check:** the four context-diagram flows to/from Student and the two to/from Bank all appear at level 0 attached to processes 1.0, 2.0, 3.0 and 4.0; no new external flow was added: the diagrams are balanced.
**Possible error:** a flow *Student record* directly from D1 Students to Bank would be illegal (store to entity): it would need a process in between.
:::

**Using DFDs in analysis:** draw the **current physical** DFD (as things are, with people and paper), derive the **current logical** DFD (what is done, no matter by whom), then the **new logical** DFD with improvements, and finally the **new physical** one. Benefits: user-friendly picture, finds missing and redundant processes. **Limitations:** no timing or control, and diagrams grow large; maintaining a **data dictionary** (definition of every flow, store, element) is essential.

### Modelling logic: decision tables, structured English, decision trees

For a process with complex rules, three techniques express its logic precisely:

**Decision table.** Conditions (stub and entries) on top, actions below; each column is a **rule**. Entries: **Y/N** for conditions, **X** for actions, **–** for "don't care".

::: example Worked example: loan approval
Conditions: *Income ≥ 50,000?* *Good credit history?* *Existing loan?* Actions: Approve, Review, Reject. With three yes/no conditions there are 2³ = **8** combinations. Combine rules that need the same action:

| Rule | R1 | R2 | R3 | R4 |
|---|---|---|---|---|
| Income ≥ 50,000? | N | Y | Y | Y |
| Good credit? | – | N | Y | Y |
| Existing loan? | – | – | N | Y |
| **Approve** | | | X | |
| **Review** | | | | X |
| **Reject** | X | X | | |

R1 covers 4 combinations (income N, anything else), R2 covers 2, R3 and R4 cover 1 each: 4 + 2 + 1 + 1 = **8**, so the table is **complete**, and no two rules overlap, so it is **consistent** (no contradiction). Reduction of "don't care" entries cut 8 columns to 4.
:::

**Structured English** writes the same logic in constrained sentences using sequence, `IF … ELSE`, `DO WHILE`/`FOR EACH`: `IF income >= 50000 AND credit = good THEN IF existing_loan THEN Review ELSE Approve ELSE Reject`. A **decision tree** draws it as a branching diagram, easier for people to follow with few conditions.

## 3.3 System data requirements: conceptual data modelling

Conceptual data modelling captures the organisation's **data**, independently of any database product, as an **entity-relationship (E-R) diagram** (introduced in the DBMS course; reviewed here at analysis depth). Gather information from interviews, forms and reports: nouns that need to be remembered are entities; descriptive facts are attributes; verbs linking nouns are relationships.

**Components:** entity types (rectangles), **attributes** (identifier underlined, multivalued, derived), **relationships** with **cardinality** (one-to-one, one-to-many, many-to-many) and **modality/participation** (mandatory or optional), **associative entities** (a relationship that carries its own attributes, such as *Enrollment* with *marks*), **weak entities**, and **unary, binary and ternary** relationships (employee *manages* employee is unary).

::: example Worked example: library
Entities: **Member**(member_id, name, phone), **Book**(isbn, title, price), **Copy**(copy_no, status), **Loan**(issue_date, due_date, return_date). Relationships: Book *has* Copy (1:N, a Copy cannot exist without its Book: mandatory on the Copy side); Member *borrows* Copy through the associative entity **Loan** (a member can borrow many copies and a copy is borrowed many times over its life: M:N resolved by Loan). Business rule: a member may hold at most 3 unreturned copies.
:::

### Supertypes and subtypes

A **supertype** has attributes common to all; **subtypes** add their own. `Person` (id, name) is the supertype of `Student` (roll_no, program) and `Teacher` (salary, subject). Subtypes inherit the supertype's attributes and relationships. Rules: **total specialisation** (every supertype instance must belong to a subtype) or **partial**; **disjoint** (one subtype only) or **overlapping**. A **subtype discriminator** attribute (e.g. `person_type`) can tell which subtype applies.

### Business rules

**Business rules** are statements that define or constrain the business: *definitions* (a "current student" is registered this semester), *facts* (a course has one teacher), *constraints* ("a student cannot enrol in more than 6 courses"), *computations* (fee = credits × rate), and *derivations* (a student passes if marks ≥ 40). They become entity relationships, cardinalities, attribute domains, triggers and application logic. Rules must be written in plain language, owned by the business and kept in the repository.

### Packaged data models and database patterns

Instead of starting from nothing, analysts can adopt a **packaged conceptual data model** supplied with an ERP package or sold as a **universal data model** (for example, models for customers, orders, products, parties and accounts). Advantages: saves analysis time, based on industry best practice. Disadvantages: may not match the organisation, must be customised. **Database patterns** (analysis patterns) are reusable small models for recurring structures: *party* (a person or organisation that plays roles such as customer, employee, supplier), *product/catalogue*, *order and order line*, *account and transaction*, *hierarchies* (bill of materials), *time-varying data* (history tables). Using a pattern avoids reinventing and reduces mistakes.

## Formula and fact sheet

- Requirements methods: interview, questionnaire, observation, documents (traditional); JAD, prototyping (contemporary); BPR (radical); user stories (agile).
- DFD elements: external entity, process, data store, data flow. Rules: no miracle/black-hole process; no flow between two entities or two stores without a process; parent and child diagrams balance.
- Decision table with n yes/no conditions has 2ⁿ combinations; complete and consistent after reduction.
- E-R: entity, attribute, relationship, cardinality, associative entity, supertype/subtype.

## Chapter summary

- Requirements are gathered by interviews, questionnaires, observation, documents, JAD, prototyping and, in agile projects, user stories; BPR rethinks processes.
- DFDs model processes in levels with strict rules and balancing; decision tables, structured English and trees model complex logic.
- Conceptual data models use E-R notation with supertypes, subtypes, business rules and reusable patterns.

## Practice

1. Differentiate functional and non-functional requirements with two examples each.
2. Compare interviews, questionnaires and observation.
3. What is JAD and when is it better than interviews?
4. Explain BPR with an example.
5. Draw (describe) the context diagram and a level-0 DFD for an online book store.
6. List the rules of DFD construction and spot the error: a data flow from a data store directly to an external entity.
7. Construct a decision table: a shop gives 10% discount if the customer is a member, and an extra 5% if the bill exceeds 5,000; non-members get 5% if the bill exceeds 5,000.
8. Draw an E-R diagram for a hospital with doctors, patients and appointments; identify the associative entity.
9. Explain supertype and subtype with an example.

::: note Answers and worked solutions
**1.** Functional: "print admit card", "calculate fee". Non-functional: "page loads in under 3 seconds", "passwords stored hashed".
**2.** See the table in 3.1: interviews give depth, questionnaires reach many cheaply, observation shows actual behaviour.
**3.** A facilitated workshop with all stakeholders that settles requirements in days; better when many stakeholders must agree and interviews would be slow and contradictory.
**4.** Redesigning a process from scratch rather than automating it, e.g. replacing a multi-signature paper leave application with one online form routed automatically.
**5.** Context: process *Online Book Store*; entities Customer, Publisher, Payment gateway; flows *Order*, *Payment details*, *Invoice*, *Purchase order*, *Stock delivery*, *Payment confirmation*. Level 0: 1.0 Process order, 2.0 Take payment, 3.0 Ship order, 4.0 Restock; stores D1 Books, D2 Orders, D3 Customers.
**6.** Rules: see 3.2. The store-to-entity flow is illegal; add a process (e.g. "Prepare report") between the store and the entity.
**7.** Conditions: Member? Bill > 5,000? Rules: Y,Y → 15%; Y,N → 10%; N,Y → 5%; N,N → 0%. Four rules for 2² = 4 combinations.
**8.** Doctor(doc_id, name, speciality), Patient(pat_id, name), **Appointment**(date, time, fee) as the associative entity resolving M:N *consults*.
**9.** Supertype Person (id, name); subtypes Student (roll_no) and Teacher (salary); each inherits id and name.
:::
