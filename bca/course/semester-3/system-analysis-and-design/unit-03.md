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

## 3.4 Three models drawn out: context, level-0 and entity-relationship

Requirements are first collected from people (Plate 3.1) and then turned into models that everyone can check. A **context diagram** (Figure 3.1) shows the whole system as one process with its external entities and the data flowing in and out; it fixes the system boundary. A **level-0 diagram** (Figure 3.2) opens that process into its main sub-processes and data stores, using the same inputs and outputs so the two levels balance. A **conceptual data model** (Figure 3.3) shows the things the system must remember and how they relate. The running example is a college library: members borrow books, and the librarian manages stock.

```photogrid label="3.1" cols="2" ratio="1.1" caption="Fact-finding for requirements. (a) An interview is the richest technique: the analyst can follow up answers and read body language. (b) The four main techniques compared."
@ photo id="bca452/interview" cap="Interview with a user"
fit 1.1
@ svg cap="Techniques compared"
f = Fig(300, 270)
rows = [("Interview", "rich detail, slow"), ("Questionnaire", "many users, shallow"), ("Observation", "real work, time"), ("Documents", "forms, reports, rules")]
for i, (a, b) in enumerate(rows):
    y = 14 + i * 62
    f.box(8, y, 284, 52, "", fill=[BLUE, "#fde68a", "#bbf7d0", "#fbcfe8"][i], stroke=NAVY)
    f.text(150, y + 18, a, size=14, color=NAVY, bold=True)
    f.text(150, y + 38, b, size=13, color=NAVY)
```

```svgfig label="3.1" caption="Context diagram of the library system. One process, two external entities (rectangles) and four data flows (arrows). Nothing inside the system is shown yet."
f = Fig(600, 190)
f.circle(300, 95, 52, fill="#bbf7d0", stroke=TEAL, sw=2.2, label="0\nLibrary\nSystem", size=12, color=NAVY)
f.box(20, 70, 120, 50, "Member", fill=BLUE, color=NAVY, size=13, bold=True)
f.box(460, 70, 120, 50, "Librarian", fill=BLUE, color=NAVY, size=13, bold=True)
f.arrow([(140, 85), (248, 85)], color=NAVY, sw=1.8, label="borrow request", lpos=(194, 72), lsize=10)
f.arrow([(248, 108), (140, 108)], color=NAVY, sw=1.8, label="issue slip, due date", lpos=(194, 124), lsize=10)
f.arrow([(460, 85), (352, 85)], color=NAVY, sw=1.8, label="new book details", lpos=(406, 72), lsize=10)
f.arrow([(352, 108), (460, 108)], color=NAVY, sw=1.8, label="overdue report", lpos=(406, 124), lsize=10)
```

```svgfig label="3.2" caption="Level-0 DFD. Processes are rounded boxes numbered 1 to 3; D1 and D2 are data stores (open boxes). Every flow touches a process, and the external flows match the context diagram, so the two levels balance."
f = Fig(600, 260)
f.box(10, 100, 90, 44, "Member", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(512, 100, 78, 44, "Librarian", fill=BLUE, color=NAVY, size=12, bold=True)
f.box(180, 24, 120, 50, "1.0 Issue book", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(180, 176, 120, 50, "2.0 Return book", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=11, bold=True)
f.box(366, 100, 124, 50, "3.0 Report overdue", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10.5, bold=True)
f.box(330, 14, 150, 28, "D1  Books", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(330, 210, 150, 28, "D2  Loans", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.arrow([(100, 112), (180, 56)], color=NAVY, sw=1.6, label="request", lpos=(122, 70), lsize=9.5)
f.arrow([(100, 134), (180, 190)], color=NAVY, sw=1.6, label="book + card", lpos=(120, 186), lsize=9.5)
f.arrow([(300, 40), (330, 30)], color=SLATE, sw=1.5, both=True)
f.arrow([(300, 206), (330, 222)], color=SLATE, sw=1.5, both=True)
f.arrow([(428, 210), (428, 150)], color=SLATE, sw=1.5)
f.arrow([(490, 125), (512, 122)], color=NAVY, sw=1.6)
f.text(551, 168, "overdue list", size=10, color=NAVY, bold=True)
f.text(300, 128, "loan record", size=9.5, color=SLATE)
```

```svgfig label="3.3" caption="Entity-relationship diagram. A member borrows many books and a book can be borrowed by many members over time (M:N), so the associative entity LOAN (issue date, due date, fine) holds each borrowing. Keys: member_id, book_id, loan_id."
f = Fig(600, 190)
f.box(10, 60, 140, 70, "MEMBER\nmember_id\nname, phone", fill=BLUE, color=NAVY, size=11, bold=True)
f.box(230, 60, 140, 70, "LOAN\nloan_id\nissue, due, fine", fill="#fde68a", stroke=AMBER, color=NAVY, size=11, bold=True)
f.box(450, 60, 140, 70, "BOOK\nbook_id\ntitle, author", fill=BLUE, color=NAVY, size=11, bold=True)
f.arrow([(150, 95), (230, 95)], color=NAVY, sw=1.8)
f.arrow([(450, 95), (370, 95)], color=NAVY, sw=1.8)
f.text(190, 84, "1 : N", size=11, color=RED, bold=True)
f.text(410, 84, "N : 1", size=11, color=RED, bold=True)
f.text(80, 150, "borrows", size=10.5, color=SLATE)
f.text(520, 150, "is borrowed", size=10.5, color=SLATE)
f.text(300, 172, "MEMBER M:N BOOK resolved by LOAN", size=11, color=TEAL, bold=True)
```

## 3.5 Eight benefits of modelling before building

1. **Shared understanding.** A diagram is easier for users and developers to read than pages of text. The librarian can check the library DFD and say at once that a return process is missing.
2. **Boundary of the system.** The context diagram states what is inside and outside the project. This stops scope creep, where extra features are added without cost or time.
3. **Early error detection.** Unbalanced flows, a process with no output or a data store nobody reads are spotted on paper. Fixing a drawing costs minutes, while fixing code costs days.
4. **Logical thinking before technology.** DFDs describe what happens to data, not which software or screen is used. The same model works whether the final system is a website, a mobile app or a desk program.
5. **Divide and conquer.** A large system is split level by level, so each analyst can study one part. A university system can be handled as admission, examination and fee sub-systems.
6. **Good database design.** An ER diagram reveals entities, keys and M:N relationships before tables are created. It shows, for example, that LOAN is needed to record each borrowing.
7. **Better communication with management.** Simple diagrams fit in a report or presentation. A sponsor can see the proposal in one page and decide whether to approve it.
8. **Reusable documentation.** Models stay valuable for maintenance and for training new staff. Years later a new developer can see how data moves through the system without reading all the code.

```photogrid label="3.2" cols="2" ratio="1.2" caption="From a full decision table to a short one. (a) A bus ticket counter, where the clerk applies the same discount rules to every passenger. (b) Four yes-or-no conditions (student, senior citizen, peak hour, advance booking) give 2 x 2 x 2 x 2 = 16 rules, and the discount can be 0, 10, 30 or 40 per cent. The 16 rules were generated from the policy and then merged by combining any two rules that differ in one condition but give the same action, which is exactly the simplification step of a decision table. The result has only 9 rules with a dash (does not matter) in many cells, and every one of the 16 original rows was checked to land on a single matching rule with the same action, so the short table is complete and consistent. The Rs and percentages are invented for the exercise, not a real Sajha or Nepal Yatayat tariff."
@ photo id="bcasad/counter" cap="A bus ticket counter: rules applied all day"
fit 1.2
focus 0.5 0.5
@ svg cap="Decision table: 16 rules merged"
import itertools
names = ["Student", "Senior", "Peak", "Advance"]
def disc(s, a, p, b):
    d = 30 if (s or a) else 0
    if b and not p:
        d += 10
    return d
rows = [(bits, disc(*bits)) for bits in itertools.product([1, 0], repeat=4)]
acts = sorted({d for _, d in rows})
def imps(mins):
    cur = {tuple(m) for m in mins}
    primes = set()
    while cur:
        nxt, used = set(), set()
        for x in cur:
            for y in cur:
                diff = [i for i in range(4) if x[i] != y[i]]
                if len(diff) == 1 and x[diff[0]] != "-" and y[diff[0]] != "-":
                    z = list(x)
                    z[diff[0]] = "-"
                    nxt.add(tuple(z))
                    used |= {x, y}
        primes |= cur - used
        cur = nxt
    return primes
def cov(imp, bits):
    return all(i == "-" or i == b for i, b in zip(imp, bits))
rules = []
for a in acts:
    mins = [b for b, d in rows if d == a]
    P = sorted(imps(mins), key=lambda p: (-p.count("-"), str(p)))
    left = set(mins)
    while left:
        best = max(P, key=lambda p: sum(cov(p, m) for m in left))
        rules.append((best, a))
        left -= {m for m in left if cov(best, m)}
for bits, d in rows:
    hit = [a for r, a in rules if cov(r, bits)]
    assert hit and set(hit) == {d}
facts = dict(n=len(rules), acts=len(acts))
f = Fig(300, 246)
f.text(150, 12, "Ticket discount: 4 conditions, %d rules left" % len(rules), size=10.5, color=NAVY, bold=True)
for i, nm in enumerate(names):
    f.box(6 + i * 52, 22, 50, 20, nm, fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3, sw=1)
f.box(214, 22, 80, 20, "Discount", fill="#fde68a", stroke=NAVY, size=10.5, bold=True, r=3, sw=1)
for r, (imp, a) in enumerate(rules):
    y = 46 + r * 18
    for i, v in enumerate(imp):
        t = "-" if v == "-" else ("Y" if v == 1 else "N")
        f.box(6 + i * 52, y, 50, 16, t, fill="#f1f5f9" if t == "-" else MINT, stroke=SLATE, size=10.5, bold=t != "-", r=2, sw=1)
    f.box(214, y, 80, 16, "%d%%" % a, fill=SAND, stroke=SLATE, size=10.5, bold=True, r=2, sw=1)
f.text(150, 46 + len(rules) * 18 + 10, "- means the answer does not matter", size=10.5, color=SLATE)
f.text(150, 238, "checked against all 16 rows: no clash", size=10.5, color=TEAL, bold=True)
```

## 3.6 Requirements determination in practice

Section 3.1 listed the techniques. This section shows how an analyst actually uses them on one project, the **admission system of a BCA college**, and ends with the document that records the result.

### Planning the fact-finding

1. List **who** knows the work: the admission officer, the accountant, the principal, applicants, the exam coordinator.
2. Decide **which technique** suits each person: interview the officer and accountant, questionnaire for 200 applicants, observation of the admission desk on the busiest day, document analysis of last year's forms and registers.
3. Prepare an **interview guide**: purpose, name and role, 8 to 12 questions, time limit, agreed follow-up.
4. After each session write **minutes within 24 hours** and send them back for confirmation.

### A sample interview guide (admission officer)

| No. | Question | Type | Why asked |
|---|---|---|---|
| 1 | Walk me through one admission from the first enquiry to the receipt. | open | gets the real process |
| 2 | Which forms and registers do you fill in? | open | finds data and documents |
| 3 | How many applicants do you handle per day in peak week? | closed | volume for design |
| 4 | What mistakes happen most often? | open | problems to fix |
| 5 | Is a scholarship checked against the entrance merit list? | closed | business rule |
| 6 | What report do you give the principal, and how often? | open | outputs |

### Questionnaire design

Keep it short (under ten questions), use closed questions with a scale where possible (for example 1 to 5), avoid leading or double-barrelled questions ("Is the form short and clear?" asks two things), pilot it with three people and state the deadline. Expect a response rate of 30 to 40 percent; send reminders.

### Observation

Observation shows the difference between the *formal* process in the manual and the *real* one on the desk. Record times for each step, interruptions and workarounds (such as photocopies kept in a drawer). Tell the staff why you are watching; do it on more than one day.

### A JAD session in outline

A one-day **JAD** workshop has a **facilitator** (neutral, controls the agenda), a **scribe** (records on screen), the **sponsor**, **users** with decision authority, **analysts** and IT staff. Agenda: objectives (30 min), walk through the current process (60 min), list problems and rank them (60 min), agree requirements and priorities using **MoSCoW** (Must, Should, Could, Won't) (90 min), summarise and assign actions (30 min). Rules: stay on agenda, one speaker at a time, decisions are recorded.

::: example Worked example: prioritising with MoSCoW
Requested features for the admission system: (1) enter applicant data, (2) print receipt, (3) SMS result to applicant, (4) online payment, (5) graph of admissions by district. **Must:** 1, 2. **Should:** 3 (the college has bulk SMS). **Could:** 5. **Won't (this release):** 4, because it needs a payment-gateway contract. Delivering the *Must* items first gives a working system even if time runs out.
:::

### Prototyping as a requirements technique

When users cannot describe a screen, show one. A paper or clickable mock-up of the admission form takes a day, and users quickly tell you "the guardian's phone is more important than the email". Treat it as a questionnaire made visible.

### User stories and acceptance criteria (agile)

Format: **As a** *role*, **I want** *goal*, **so that** *benefit*. A good story is **INVEST**: Independent, Negotiable, Valuable, Estimable, Small, Testable.

::: example Worked example: one story with acceptance criteria
**Story:** As an admission officer, I want to print a receipt after payment so that the applicant has proof. **Acceptance criteria:** (1) receipt shows receipt number, name, program, amount in figures and words, date; (2) receipt number is unique and in sequence; (3) printing twice marks the second copy "DUPLICATE"; (4) cannot print before payment is saved.
:::

### From notes to a Software Requirements Specification (SRS)

An SRS (IEEE 830 style) has: **1 Introduction** (purpose, scope, definitions), **2 Overall description** (product perspective, user classes, constraints, assumptions), **3 Specific requirements** (functional requirements with IDs such as FR-12, external interfaces, non-functional requirements: performance, security, reliability, usability), **4 Appendices**. Each requirement must be **correct, unambiguous, complete, consistent, verifiable and traceable**. Compare "The system should be fast" (not verifiable) with "A receipt prints within 3 seconds for 95 percent of requests" (verifiable).

**Likely questions.** (a) Compare interview, questionnaire and observation (5). (b) Explain JAD with its roles and its advantages (10). (c) What is an SRS? State six qualities of a good requirement (5).

## 3.7 Decision tables, supertypes, business rules and packaged models

### Modelling logic with decision tables

A **decision table** lists **conditions**, **actions** and **rules** (columns). It is used when many conditions combine into different actions and a DFD or text description would hide the combinations. With *n* two-valued conditions there are **2ⁿ** rules; **rule reduction** merges rules that give the same action by using a dash for "does not matter".

::: example Worked example: scholarship decision table
Conditions: C1 entrance score at least 70? C2 family income below Rs 300,000? C3 woman or marginalised group? Actions: A1 full scholarship, A2 half scholarship, A3 none.

| Rule | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| C1 score ≥ 70 | Y | Y | Y | N | N |
| C2 income low | Y | Y | N | Y | N |
| C3 woman/marginalised | Y | N | - | - | - |
| **A1 full** | X | | | | |
| **A2 half** | | X | | X | |
| **A3 none** | | | X | | X |

With three conditions there are 2³ = 8 rules. Merging gives the five shown: R3 covers Y,N,Y and Y,N,N; R4 covers N,Y,Y and N,Y,N; R5 covers N,N,Y and N,N,N. Rule check: 1 + 1 + 2 + 2 + 2 = 8, so no combination is missing and none is repeated.
:::

A **decision tree** shows the same logic as branches and is easier to read for a few conditions. **Structured English** writes it as IF/THEN/ELSE. Use the table to *check completeness*, the tree to *explain*.

### Supertypes and subtypes in the ER model

A **supertype** holds attributes common to several entities, and **subtypes** hold the attributes specific to each. Example: PERSON (id, name, address) is the supertype; STUDENT (program, roll) and TEACHER (department, salary) are subtypes. Rules: **total specialisation** (every PERSON must be one of the subtypes) or **partial**; **disjoint** (a person can be only one subtype) or **overlapping** (a person can be both a student and a teacher).

```svgfig label="3.4" caption="Supertype and subtypes. PERSON holds the shared attributes; STUDENT and TEACHER inherit them and add their own. The 'd' in the circle means disjoint: one person plays one role at a time."
f = Fig(600, 230)
f.box(200, 14, 200, 66, "PERSON\nperson_id, name\naddress, phone", fill=BLUE, color=NAVY, size=12, bold=True)
f.circle(300, 120, 14, fill="#fde68a", stroke=AMBER, label="d", size=12, color=NAVY)
f.line(300, 80, 300, 106, color=NAVY, sw=1.8)
f.line(300, 134, 130, 160, color=NAVY, sw=1.8)
f.line(300, 134, 470, 160, color=NAVY, sw=1.8)
f.box(40, 160, 180, 56, "STUDENT\nprogram, roll_no", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=12, bold=True)
f.box(380, 160, 180, 56, "TEACHER\ndepartment, salary", fill="#bbf7d0", stroke=TEAL, color=NAVY, size=12, bold=True)
```

### Business rules

A **business rule** is a statement that defines or constrains some aspect of the business. Kinds: **term** (a "member" is a person with a valid card), **fact** (a loan has one member and one book), **constraint** (a member may borrow at most 3 books), **derivation** (fine = overdue days × Rs 5), **inference** (if fines exceed Rs 500, the card is blocked). Rules are collected from policy documents and interviews, written in plain atomic sentences, stored in a rule repository and turned into ER constraints, validation code or database triggers.

### Packaged conceptual data models and database patterns

Instead of starting from nothing, analysts adopt **packaged data models**: industry or vendor models of common entities (customer, order, account, invoice) and **database patterns** such as *party* (a single PARTY entity with roles for customer, supplier and employee), *product catalogue*, *order and line item* and *hierarchy* (an entity related to itself). Advantages: faster, proven, fewer omissions. Disadvantages: not tailored, may be too general, licence cost. Always check the packaged model against your own business rules before adopting it.

**Likely questions.** (a) Construct a decision table for a loan approval policy and reduce it (10). (b) Explain supertype and subtype with an ER diagram (5). (c) What are business rules? Give four kinds (5). (d) Advantages and disadvantages of packaged data models (5).

## 3.8 A level-1 decomposition, the data dictionary and the CRUD check, worked end to end

Sections 3.2 and 3.4 drew the context diagram and level 0 of the library system. Analysis does not stop there: a process such as *Issue book* hides decisions that a programmer must know, and the data flows hide structure that a database designer must know. Three more artefacts close the gap: the **level-1 DFD**, the **data dictionary** and the **process specification**. A fourth, the **CRUD matrix**, then checks that all the models agree.

### Level-1 DFD of process 1.0 Issue book

Decomposition replaces one process by its child diagram. The children are numbered 1.1, 1.2 and so on, the data stores that the parent touched appear again, and the flows that cross the parent's boundary must be the same flows in the child diagram. That is **balancing**: Figure 3.5 shows no new external flow, only the member's request in and the slip out.

```svgfig label="3.5" caption="Level-1 DFD of process 1.0 Issue book. The parent had one input (request) and one output (issue slip); the child diagram has the same two external flows, so it is balanced. D1 Members, D2 Books and D3 Loans are the stores seen in the level-0 diagram."
f = Fig(680, 262)
f.box(4, 100, 62, 44, "Member", fill=BLUE, color=NAVY, size=11, bold=True)
labs = ["1.1\nVerify\nmember", "1.2\nCheck\navailability", "1.3\nRecord\nloan", "1.4\nPrint\nslip"]
px = [112, 246, 380, 514]
for x, l in zip(px, labs):
    f.box(x, 96, 90, 52, l, fill="#bbf7d0", stroke=TEAL, color=NAVY, size=10.5, bold=True)
f.box(112, 14, 90, 28, "D1 Members", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.box(246, 14, 90, 28, "D2 Books", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.box(380, 14, 90, 28, "D3 Loans", fill="#fde68a", stroke=AMBER, color=NAVY, size=10.5, bold=True)
f.arrow([(66, 122), (112, 122)], color=NAVY, sw=1.6)
f.text(89, 104, "member,\nbook id", size=9, color=SLATE)
f.arrow([(202, 122), (246, 122)], color=NAVY, sw=1.6)
f.text(224, 106, "valid\nmember", size=9, color=SLATE)
f.arrow([(336, 122), (380, 122)], color=NAVY, sw=1.6)
f.text(358, 106, "copy\nfree", size=9, color=SLATE)
f.arrow([(470, 122), (514, 122)], color=NAVY, sw=1.6)
f.text(492, 106, "loan\ndetails", size=9, color=SLATE)
f.arrow([(157, 42), (157, 96)], color=SLATE, sw=1.5)
f.arrow([(291, 42), (291, 96)], color=SLATE, sw=1.5)
f.arrow([(425, 96), (425, 42)], color=SLATE, sw=1.5)
f.arrow([(396, 96), (334, 42)], color=SLATE, sw=1.5)
f.arrow([(559, 148), (559, 200), (35, 200), (35, 144)], color=NAVY, sw=1.6)
f.text(300, 216, "issue slip", size=10, color=NAVY, bold=True)
f.text(340, 246, "A flow arrow from a store to a process is a read; from a process to a store, a write.", size=9.5, color=SLATE)
```

### The data dictionary

A DFD names flows and stores, but a name is not a definition. The **data dictionary (DD)** defines every flow, store and element exactly once, so that analysts, programmers and users mean the same thing. The classic notation uses a few symbols:

| Symbol | Meaning | Example |
|---|---|---|
| `=` | is composed of | `Member = Member_ID + Name` |
| `+` | and (sequence) | `Name = First + Last` |
| `( )` | optional element | `Member = ... + (Email)` |
| `{ }` | repetition (with limits `n{ }m`) | `1{Book_ID}3` : one to three books |
| `[ ]` | selection: one of the listed choices, separated by a vertical bar | `Contact = [Mobile / Landline]` (bar shown as a slash in this table) |
| `* *` | comment | `* Nepal numbers start with 98 or 97 *` |

```text
Issue_Slip   = Slip_No + Issue_Date + Member_ID + Member_Name + 1{Book_ID + Title}3 + Due_Date
Due_Date     = Issue_Date + 14 days                       * rule from the library policy *
Member       = Member_ID + Name + Phone + (Email) + Status
Status       = [Active | Suspended | Expired]
Member_ID    = 4 digits                                   * for example 0173 *
Book_ID      = Accession_No                               * unique per physical copy *
```

Read the first line aloud: an issue slip is a slip number, an issue date, the member's number and name, one to three books each with a book number and a title, and a due date. Writing the dictionary often exposes mistakes: if two analysts define *Due_Date* differently, a programmer would have built two systems. In a CASE tool the dictionary is the **repository** that also feeds the screens and the database schema.

### Process specification

A process that is no longer decomposed (a **primitive** process) needs a **process specification**: its logic written precisely in structured English, a decision table or a decision tree (3.2, 3.7).

```text
PROCESS 1.3  Record loan
  IF member has fewer than 3 open loans AND the copy is available
      create a Loan row with Due_Date = today + 14 days
      mark the Book as Issued
  ELSE
      refuse the loan and show the reason (limit reached, or copy issued)
  END IF
```

### Common DFD errors

- **Black hole:** a process with inputs but no output (it consumes data and produces nothing).
- **Miracle:** a process with outputs but no input (it invents data).
- **Gray hole:** the outputs cannot be produced from the inputs (printing *Due_Date* when no issue date flows in).
- **Illegal flows:** entity to entity, entity to store, or store to store without a process in between.
- **Unbalanced child:** flows at the child level that do not appear at the parent.
- **Unnamed or vague flows**, such as *data* or *information*.

### The CRUD matrix: checking models against each other

A **CRUD matrix** lists processes in rows and data stores (or entities) in columns, and writes C (create), R (read), U (update) or D (delete) where a process touches the data. It joins the process model (DFD) to the data model (ER) and reveals gaps.

| Process | D1 Members | D2 Books | D3 Loans |
|---|---|---|---|
| 1.1 Verify member | R | | |
| 1.2 Check availability | | R | |
| 1.3 Record loan | | U | C |
| 1.4 Print slip | R | | R |
| 2.0 Return book | | U | U |
| 3.0 Report overdue | R | | R |
| 4.0 Maintain members | C, R, U, D | | |
| 5.0 Maintain catalogue | | C, R, U, D | |

Read it by column: **every store needs at least one C** (otherwise nothing ever fills it: before row 5.0 was added, *D2 Books* had no C and the matrix exposed a missing process), **at least one R** (otherwise nobody uses the data), and a **D or an archiving rule** (otherwise it grows for ever). D3 Loans has no D on purpose: loans are kept as history, so the missing delete is a decision to record, not a gap. Read it by row too: a process with no C, U or D is only a report, and one that updates many stores deserves a closer look because it must be done as a single **transaction**.

## 3.9 Requirement quality: writing, reviewing, ranking and tracing

A design can only be as good as the requirement behind it. Industry studies repeatedly find that a large share of project defects start as missing, vague or contradictory requirements, which is why Figure 1.1 puts the cost multiplier of a late fix so high. This section turns "gather requirements" into a checkable craft.

### What a good requirement looks like

A good requirement is **necessary** (a stakeholder needs it), **unambiguous** (one reading only), **verifiable** (a test can say pass or fail), **consistent** with the others, **feasible** and **traceable** to its source. Four weak habits spoil these qualities:

| Weak wording | Why it fails | Rewritten and testable |
|---|---|---|
| The system shall be fast. | "fast" cannot be tested | Search results shall appear within 2 seconds for 95 per cent of queries with 50 users online. |
| The system shall be user friendly. | opinion, not measurement | A new clerk shall register a student in under 3 minutes after 30 minutes of training. |
| The system shall support all browsers. | "all" is infinite | The system shall work in the two latest versions of Chrome, Firefox and Edge. |
| Fees and fines shall be calculated and printed and exported. | three requirements in one sentence | Split: R12 calculate fee; R13 print receipt; R14 export fee list to CSV. |

Words that usually signal trouble: *fast, easy, flexible, adequate, as appropriate, etc., and/or, should (when you mean shall), all, never*. Use **shall** for mandatory, **should** for desirable and **may** for optional, and give every requirement a unique identifier (R1, R2, ...).

### The FURPS+ checklist

**FURPS+** reminds the analyst to ask beyond the functions:

- **F**unctionality: features, security, rules.
- **U**sability: ease of learning, help, accessibility (Nepali language support, screen size).
- **R**eliability: availability, recovery, accuracy (the system shall lose no more than 5 minutes of data after a crash).
- **P**erformance: response time, throughput, capacity.
- **S**upportability: maintainability, portability, configurability.
- **+** constraints: legal (Electronic Transactions Act), design, implementation, interface and physical limits.

### Reviewing requirements

Requirements are reviewed before design begins, in increasing order of formality: a **desk check** by the author, a **walkthrough** where the author leads peers through the document, and an **inspection** where trained reviewers with checklists look for defects and record them. Cheap and effective checks are: have two analysts write a test for the same requirement and compare; read the document backwards; ask the users to explain each requirement in their own words.

### Ranking requirements

Not everything can be built in the first release, so requirements are ranked. **MoSCoW** puts each in Must have, Should have, Could have or Won't have this time. The **Kano model** adds a view of satisfaction: *basic* needs cause anger when missing but no delight when present (the result system must calculate the grade correctly); *performance* needs raise satisfaction in proportion (faster result publishing); *delighters* are unexpected extras (an SMS alert with the result). The **100-point method** gives each stakeholder 100 points to spread across the requirements and adds up the totals. Ranking is a negotiation, so it is recorded with the reason.

### The requirements traceability matrix

A **traceability matrix** links each requirement forward to the design element, code module and test case that satisfy it, and backward to the stakeholder who asked for it. It answers two questions at any time: *is every requirement covered by a test?* and *does every test and feature serve a requirement?* A change request is judged by following its row to see what would be touched.

| Req. | Statement (short) | Source | Priority | Design element | Test case |
|---|---|---|---|---|---|
| R1 | Verify membership before a loan | Librarian | Must | Process 1.1, D1 Members | TC-01, TC-02 |
| R2 | Refuse a loan at 3 open loans | Policy 4.2 | Must | Process 1.3 rule | TC-05 |
| R3 | Due date is 14 days after issue | Policy 4.3 | Must | DD: Due_Date | TC-06 |
| R4 | Overdue list on demand | Principal | Should | Process 3.0 | TC-11 |
| R5 | SMS reminder 2 days before due | Members | Could | not designed yet | none yet |

A row with an empty test column (R5) is not an error if the requirement is not scheduled, but a **Must** with no test is a defect in the plan. The matrix also ties this unit to unit 5: the test cases in 5.7 are written from the same requirement numbers.

::: example Worked example: finding the defects in a requirement set
Requirement set for a hostel booking system: (R1) The system shall be easy to use. (R2) A student shall be able to book a room and pay online and cancel. (R3) The system shall never be down. (R4) Rooms shall be shown to students.
Defects found: **R1** unverifiable (rewrite with a task time); **R2** three requirements fused (split into book, pay, cancel); **R3** infeasible and unmeasurable (rewrite: availability of 99.5 per cent per month, outside a Saturday maintenance window); **R4** incomplete (which rooms? only vacant ones? by which filters?). Four requirements, four defects, found before a single line of code was written: that is the return on a review.
:::

## Formula and fact sheet

- Requirements methods: interview, questionnaire, observation, documents (traditional); JAD, prototyping (contemporary); BPR (radical); user stories (agile).
- DFD elements: external entity, process, data store, data flow. Rules: no miracle/black-hole process; no flow between two entities or two stores without a process; parent and child diagrams balance.
- Decision table with n yes/no conditions has 2ⁿ combinations; complete and consistent after reduction.
- E-R: entity, attribute, relationship, cardinality, associative entity, supertype/subtype.
- Data dictionary symbols: = is composed of, + and, ( ) optional, { } repetition, [ | ] selection. DFD errors: black hole, miracle, gray hole.
- CRUD matrix: every store needs a C and an R. A good requirement is necessary, unambiguous, verifiable, consistent, feasible and traceable.

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
10. Decompose process 2.0 Return book of the library DFD into child processes and check that the child is balanced.
11. Write data dictionary entries for Fee_Receipt (receipt number, date, student, one or more payments) and for Phone (mobile or landline).
12. Name the DFD error in each: (a) a process that only receives data; (b) a process that prints a total without any amounts flowing in; (c) a flow from one store to another.
13. Build a CRUD matrix for the processes Register student, Collect fee, Print dues list against the stores Students and Payments, and say what is missing.
14. Rewrite as testable requirements: (a) The portal shall be fast. (b) The system shall be secure.
15. List four defects in: R1 The report shall be adequate. R2 The system shall import, validate and archive marks.

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
**10.** Children: 2.1 Find loan, 2.2 Calculate fine (if late), 2.3 Update loan and book. The child has only the flows of the parent: *returned book* in, *receipt (fine)* out, with D2 Books and D3 Loans as stores. No new external flow, so it is balanced.
**11.** `Fee_Receipt = Receipt_No + Date + Student_ID + Student_Name + 1{Fee_Head + Amount} + Total`. `Phone = [Mobile | Landline]`, with the comment `* Mobile starts with 98 or 97 *`.
**12.** (a) Black hole. (b) Gray hole (or miracle if there are no inputs at all). (c) Illegal flow: a store cannot send data directly to another store; a process is needed.
**13.** Register student: Students C. Collect fee: Students R, Payments C. Print dues list: Students R, Payments R. Missing: no process updates or deletes a student record (add Maintain student), and Payments is never corrected (add Cancel or adjust payment, or record the choice not to).
**14.** (a) The portal shall display a student's result within 3 seconds for 95 per cent of requests with 200 users online. (b) Passwords shall be stored as salted hashes; an account shall be locked after 5 failed logins within 10 minutes.
**15.** R1: "adequate" is unverifiable. R2: three requirements fused; "import, validate and archive" are not separately testable; no format, volume or time stated; no identifier of source or priority.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). What is a data flow diagram? Explain its four symbols and the rules for drawing a correct DFD.**

*Introduction.* A data flow diagram (DFD) is a graphical model that shows how data moves through a system: where it comes from, how it is processed, where it is stored and where it goes (Figures 3.1 and 3.2).

*Symbols.*

1. **Process.** A rounded box (or circle) that transforms data, named with a verb phrase and numbered, for example *1.0 Issue book*.
2. **Data flow.** An arrow carrying named data between elements.
3. **Data store.** An open-ended box, such as *D1 Books*, where data rests.
4. **External entity.** A rectangle outside the system that supplies or receives data, such as *Member*.

*Rules.*

5. Every process has at least one input and one output; no process only consumes or only creates data.
6. Data cannot flow directly between two entities, between two stores, or between a store and an entity; a process must lie between.
7. Every flow is named and every store has a name.
8. Parent and child diagrams must balance: the child's external flows equal the parent's.

| Symbol | Shape | Example |
|---|---|---|
| Process | rounded box | 1.0 Issue book |
| Data flow | arrow | borrow request |
| Data store | open box | D1 Books |
| Entity | rectangle | Member |

*Conclusion.* A DFD shows what the system does with data, independent of technology, and balanced levels let large systems be explained step by step.

**Q2 (10 marks). For a college library, draw the context diagram, explain the level-0 DFD, and draw an entity-relationship diagram that includes the many-to-many relationship between members and books.**

*Introduction.* Process modelling (DFD) and data modelling (ERD) are the two main analysis models. The DFD shows data in motion; the ERD shows data at rest.

*Context diagram (Figure 3.1).* The whole system is one process, *0 Library System*. The external entities are the **Member** and the **Librarian**. Flows: *borrow request* and *issue slip with due date* between member and system; *new book details* and *overdue report* between librarian and system.

*Level-0 DFD (Figure 3.2).* The system opens into three processes:

1. **1.0 Issue book:** receives the request, checks the book in **D1 Books**, records the loan in **D2 Loans** and returns the issue slip.
2. **2.0 Return book:** receives the book and card, updates the loan and the book's availability, and calculates any fine.
3. **3.0 Report overdue:** reads the loans store and sends the overdue list to the librarian.

The external flows match those of the context diagram, so the two levels are balanced.

*Entity-relationship diagram (Figure 3.3).*

4. **Entities.** MEMBER (member_id, name, phone) and BOOK (book_id, title, author).
5. **Relationship.** A member may borrow many books over time, and a book is borrowed by many members over time: **M:N**.
6. **Resolution.** A many-to-many relationship cannot be stored directly in a relational table, so an associative entity **LOAN** (loan_id, member_id, book_id, issue_date, due_date, fine) is created. Now MEMBER 1:N LOAN and BOOK 1:N LOAN.
7. **Keys.** Primary keys: member_id, book_id, loan_id. Foreign keys in LOAN: member_id, book_id.
8. **Normalisation.** Member and book details are stored once, so no repeating groups or update anomalies arise.

| Aspect | DFD | ERD |
|---|---|---|
| Shows | data in motion | data at rest |
| Main symbols | process, flow, store, entity | entity, attribute, relationship |
| Question | What happens to data? | What must be remembered? |
| Becomes | programs and modules | database tables |

*Conclusion.* The context and level-0 diagrams define the processes and the boundary; the ER diagram with the LOAN entity defines the database. Together they form the logical model from which design begins.
