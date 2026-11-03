---
subject: Project I
grade: BCA Semester 4
unit: 3
title: Analysis and Design: Requirements, DFD, ER and Screens
area: BCA 256 · Project I · Unit 3
---

Design is thinking on paper, where mistakes cost minutes instead of weeks. This unit takes the scope of Unit 1 and produces the four documents that every Project I report needs: the requirements list, a use-case diagram, data-flow diagrams (DFD) and an entity-relationship (ER) diagram with a database schema, plus screen sketches.

::: key What this unit gives you
- Functional and non-functional requirements with testable wording.
- A use-case diagram and level 0 and level 1 DFDs for CampusShelf.
- An ER diagram, a relational schema created and checked by a real script.
- Three wireframes and the eight benefits of designing before coding.
:::

## 3.1 Requirements: what the system must do

A **functional requirement** states something the system does ("the system shall calculate a fine"). A **non-functional requirement** states how well it does it (speed, security, usability). Each must be **testable**: a tester should be able to say pass or fail.

| ID | Type | Requirement | How it is tested |
|---|---|---|---|
| F1 | functional | The librarian logs in with a user name and password. | wrong password is rejected |
| F2 | functional | The librarian adds, edits and searches books and members. | add a book, find it by title |
| F3 | functional | The system issues a book for 14 days if a copy is available. | issue the last copy, next issue refused |
| F4 | functional | On return, fine = Rs 2 × days beyond the due date. | return 5 days late, fine is Rs 10 |
| F5 | functional | The system lists all overdue books. | one overdue loan appears |
| N1 | non-functional | Issue or return completes in under 30 seconds. | stopwatch on 20 transactions |
| N2 | non-functional | Passwords are stored only as salted hashes. | inspect the database file |
| N3 | non-functional | A new librarian can learn the screens in 15 minutes. | trial with one user |

**User stories** are a friendly form: "As a librarian, I want to see overdue books, so that I can remind students." Write one per functional requirement and tick them off at the demo.

## 3.2 Use-case diagram

A **use-case diagram** shows who (the **actors**) uses which functions of the system (the **use cases**), inside a boundary box. It is the cleanest way to show the examiner the whole system on one page.

```svgfig label="3.1" caption="Use-case diagram of CampusShelf. The librarian (left) performs six use cases; the student (right) can only search the catalogue and see his or her own loans. The box is the system boundary."
f = Fig(780, 330)
f.box(170, 5, 440, 320, "", fill="#f8fafc", stroke=SLATE)
f.text(390, 22, "CampusShelf", size=11.5, color=SLATE, bold=True)
left = ["Log in", "Manage books", "Manage members", "Issue book", "Return book and fine", "Overdue report"]
for i, n in enumerate(left):
    f.box(190, 40 + i*47, 190, 34, n, fill=BLUE, stroke=NAVY, size=11, bold=True)
    f.line(105, 165, 190, 57 + i*47, color=NAVY, sw=1.2)
for i, n in enumerate(["Search catalogue", "View my loans"]):
    f.box(410, 110 + i*100, 180, 34, n, fill=SOFT, stroke=TEAL, size=11, bold=True)
    f.line(675, 165, 590, 127 + i*100, color=TEAL, sw=1.2)
for x, nm in [(70, "Librarian"), (705, "Student")]:
    f.circle(x, 135, 14, fill=SOFT, stroke=NAVY)
    f.line(x, 149, x, 190, color=NAVY, sw=2); f.line(x - 24, 162, x + 24, 162, color=NAVY, sw=2)
    f.line(x, 190, x - 18, 220, color=NAVY, sw=2); f.line(x, 190, x + 18, 220, color=NAVY, sw=2)
    f.text(x, 242, nm, size=12, color=NAVY, bold=True)
```

## 3.3 Data-flow diagrams: how data moves

A **DFD** shows how data flows between **external entities** (people or systems outside), **processes** (circles that transform data), **data stores** (open boxes where data rests) and **flows** (labelled arrows). It never shows loops, decisions or code; only data.

- **Level 0 (context diagram):** the whole system is one process, with every external entity and the flows in and out.
- **Level 1:** the single process is exploded into three to seven main processes and the data stores.
- **Rules:** every flow has a name; a process has at least one input and one output; data stores connect only to processes; a level 1 diagram must have the same external flows as level 0 (*balancing*).

```svgfig label="3.2" caption="Level 0 DFD (context diagram) of CampusShelf. The whole system is one process; the librarian and the student are external entities. Every arrow carries a named piece of data."
f = Fig(780, 200)
f.box(20, 70, 120, 56, "Librarian", fill=SOFT, stroke=NAVY, size=12, bold=True)
f.box(640, 70, 120, 56, "Student", fill=SOFT, stroke=NAVY, size=12, bold=True)
f.circle(390, 98, 72, fill=BLUE, stroke=NAVY, label="0\nCampusShelf", size=12)
f.arrow([(140, 84), (318, 84)], color=NAVY, label="book, member, issue, return data", lpos=(229, 70))
f.arrow([(318, 114), (140, 114)], color=TEAL, label="receipts, fines, overdue list", lpos=(229, 132))
f.arrow([(640, 84), (462, 84)], color=NAVY, label="search request", lpos=(551, 70))
f.arrow([(462, 114), (640, 114)], color=TEAL, label="availability, due dates", lpos=(551, 132))
f.text(390, 190, "Level 0: one process, two external entities", size=10.5, color=SLATE)
```

```svgfig label="3.3" caption="Level 1 DFD of CampusShelf. The context process splits into three processes that share three data stores (D1 Books, D2 Members, D3 Issues). The external flows match Figure 3.2, so the two levels are balanced."
f = Fig(780, 320)
f.box(10, 130, 110, 50, "Librarian", fill=SOFT, stroke=NAVY, size=12, bold=True)
f.box(660, 20, 110, 50, "Student", fill=SOFT, stroke=NAVY, size=12, bold=True)
for i, nm in enumerate(["1.0 Manage\ncatalogue", "2.0 Issue and\nreturn", "3.0 Overdue\nreports"]):
    f.circle(270, 55 + i*105, 48, fill=BLUE, stroke=NAVY, label=nm, size=10.5)
for i, nm in enumerate(["D1  Books", "D2  Members", "D3  Issues"]):
    f.box(470, 38 + i*105, 120, 34, nm, fill=SOFT, stroke=AMBER, size=11, bold=True)
f.arrow([(120, 145), (224, 70)], color=NAVY, label="book, member data", lpos=(160, 92))
f.arrow([(120, 155), (222, 150)], color=NAVY, label="issue, return", lpos=(172, 142))
f.arrow([(222, 262), (120, 175)], color=TEAL, label="overdue list", lpos=(128, 232))
f.arrow([(318, 55), (470, 55)], color=NAVY, both=True, label="read / write", lpos=(394, 45))
f.arrow([(310, 128), (472, 78)], color=NAVY, label="stock", lpos=(380, 88))
f.arrow([(318, 160), (470, 160)], color=NAVY, both=True, label="member check", lpos=(394, 177))
f.arrow([(305, 190), (472, 250)], color=NAVY, label="loan record", lpos=(366, 238))
f.arrow([(470, 275), (318, 275)], color=TEAL, label="due dates", lpos=(394, 292))
f.arrow([(660, 52), (592, 52)], color=NAVY, label="search", lpos=(626, 40))
f.text(390, 314, "Three processes, three data stores, two external entities", size=10.5, color=SLATE)
```

## 3.4 The ER diagram and the database schema

An **entity-relationship (ER) diagram** shows the things the system stores (**entities**), their properties (**attributes**) and how they relate (**cardinality**: 1 to many, many to many). A *many-to-many* relationship, such as "a student borrows many books and a book is borrowed by many students over time", becomes its own table (here `issue`), which also holds facts about the event: dates and fine.

```svgfig label="3.4" caption="ER diagram of CampusShelf. MEMBER and BOOK are linked many-to-many through ISSUE, which records each loan. PK = primary key, FK = foreign key. One member has many issues (1 to N); one book has many issues (1 to N)."
f = Fig(780, 250)
def ent(x, y, w, title, rows):
    h = 34 + 22*len(rows)
    f.box(x, y, w, h, "", fill="#ffffff", stroke=NAVY)
    f.box(x, y, w, 30, title, fill=BLUE, stroke=NAVY, size=12, bold=True)
    for i, r in enumerate(rows):
        f.text(x + 10, y + 46 + i*22, r, size=11, color=NAVY, anchor="start")
ent(20, 20, 200, "MEMBER", ["PK member_id", "name", "program", "phone"])
ent(290, 20, 200, "ISSUE", ["PK issue_id", "FK member_id", "FK book_id", "issue_date", "due_date", "return_date", "fine"])
ent(560, 20, 200, "BOOK", ["PK book_id", "title", "author", "copies"])
f.line(220, 70, 290, 70, color=TEAL, sw=2); f.line(490, 70, 560, 70, color=TEAL, sw=2)
f.text(232, 62, "1", size=12, color=RED, bold=True); f.text(278, 62, "N", size=12, color=RED, bold=True)
f.text(502, 62, "N", size=12, color=RED, bold=True); f.text(548, 62, "1", size=12, color=RED, bold=True)
f.text(255, 90, "borrows", size=10.5, color=TEAL, italic=True); f.text(525, 90, "is lent", size=10.5, color=TEAL, italic=True)
f.text(390, 232, "Many-to-many (member and book) resolved by the associative table ISSUE", size=10.5, color=SLATE)
```

The schema is created and checked by the next script: it lists the tables, shows the foreign keys and proves that the database refuses a loan for a member who does not exist.

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.execute("PRAGMA foreign_keys = ON")
db.executescript("""
CREATE TABLE member (member_id INTEGER PRIMARY KEY, name TEXT NOT NULL, program TEXT, phone TEXT);
CREATE TABLE book   (book_id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT, copies INTEGER CHECK (copies >= 0));
CREATE TABLE issue  (issue_id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL REFERENCES member(member_id),
    book_id   INTEGER NOT NULL REFERENCES book(book_id),
    issue_date TEXT NOT NULL, due_date TEXT NOT NULL, return_date TEXT, fine INTEGER DEFAULT 0);
""")
for (t,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"):
    cols = [c[1] for c in db.execute(f"PRAGMA table_info({t})")]
    print(f"{t:7s}", ", ".join(cols))
print("foreign keys of issue:", [(r[2], r[3]) for r in db.execute("PRAGMA foreign_key_list(issue)")])
try:
    db.execute("INSERT INTO issue (member_id, book_id, issue_date, due_date) VALUES (99, 1, '2082-01-01', '2082-01-15')")
except sqlite3.IntegrityError as e:
    print("rejected:", e)
```
```output
book    book_id, title, author, copies
issue   issue_id, member_id, book_id, issue_date, due_date, return_date, fine
member  member_id, name, program, phone
foreign keys of issue: [('book', 'book_id'), ('member', 'member_id')]
rejected: FOREIGN KEY constraint failed
```
**Normalisation check.** Every table has a primary key and each non-key column depends on the whole key and nothing else (third normal form): a book's title lives only in `book`, a member's name only in `member`. That is why the loan table stores IDs, not names.

## 3.5 Screen design: wireframes

A **wireframe** is a boxes-and-labels sketch of a screen. Draw it before coding; it takes ten minutes and prevents a week of changed layouts. Show it to the librarian and ask "can you do your job with this?".

```photogrid label="3.1" cols="3" ratio="1.0" caption="Wireframes of the three main CampusShelf screens. (a) Login. (b) Issue book: enter member and book IDs; the system checks availability and shows the due date. (c) Overdue report: the librarian sees who owes which book and the fine so far."
@ svg cap="Login screen"
f = Fig(250, 250)
f.box(10, 10, 230, 230, "", fill="#ffffff", stroke=SLATE)
f.box(10, 10, 230, 34, "CampusShelf", fill=BLUE, stroke=SLATE, size=13, bold=True)
f.text(30, 78, "User name", size=12, color=NAVY, anchor="start")
f.box(30, 88, 190, 30, "librarian", fill="#f8fafc", stroke=SLATE, size=12)
f.text(30, 148, "Password", size=12, color=NAVY, anchor="start")
f.box(30, 158, 190, 30, "••••••", fill="#f8fafc", stroke=SLATE, size=12)
f.box(75, 200, 100, 30, "Log in", fill=SOFT, stroke=TEAL, size=13, bold=True)
@ svg cap="Issue book screen"
f = Fig(250, 250)
f.box(10, 10, 230, 230, "", fill="#ffffff", stroke=SLATE)
f.box(10, 10, 230, 34, "Issue book", fill=BLUE, stroke=SLATE, size=13, bold=True)
f.text(26, 72, "Member ID", size=12, color=NAVY, anchor="start")
f.box(110, 56, 120, 28, "1042", fill="#f8fafc", stroke=SLATE, size=12)
f.text(26, 112, "Book ID", size=12, color=NAVY, anchor="start")
f.box(110, 96, 120, 28, "318", fill="#f8fafc", stroke=SLATE, size=12)
f.text(26, 152, "Due date", size=12, color=NAVY, anchor="start")
f.box(110, 136, 120, 28, "+14 days", fill="#e5e7eb", stroke=SLATE, size=12)
f.box(70, 178, 110, 30, "Issue", fill=SOFT, stroke=TEAL, size=13, bold=True)
f.text(125, 228, "2 copies left", size=11, color=TEAL)
@ svg cap="Overdue report"
f = Fig(250, 250)
f.box(10, 10, 230, 230, "", fill="#ffffff", stroke=SLATE)
f.box(10, 10, 230, 34, "Overdue books", fill=BLUE, stroke=SLATE, size=13, bold=True)
f.text(22, 66, "Member", size=11, color=SLATE, bold=True, anchor="start")
f.text(112, 66, "Book", size=11, color=SLATE, bold=True, anchor="start")
f.text(190, 66, "Fine", size=11, color=SLATE, bold=True, anchor="start")
for i, (a, b, c) in enumerate([("Asha", "C Prog.", "Rs 10"), ("Ram", "DBMS", "Rs 24"), ("Sita", "Maths I", "Rs 4")]):
    y = 92 + i*34
    f.line(18, y - 14, 232, y - 14, color="#cbd5e1", sw=0.8)
    f.text(22, y, a, size=12, color=NAVY, anchor="start"); f.text(112, y, b, size=12, color=NAVY, anchor="start"); f.text(190, y, c, size=12, color=RED, anchor="start", bold=True)
f.box(60, 200, 130, 28, "Print list", fill=SOFT, stroke=TEAL, size=12, bold=True)
```

## 3.6 Eight benefits of designing before coding

1. **Cheaper mistakes.** Changing a box on a diagram takes a minute; changing a finished database takes days. Studies of software projects repeatedly show that errors found late cost many times more to fix. Draw first, code second.
2. **A shared picture for the team.** The DFD and ER diagram show every member the same system. Arguments end when the diagram is clear. This is vital when three students code three modules.
3. **Better questions to the user.** A wireframe shown to the librarian brings real feedback: "we also record the shelf number". It is far easier to add a field to a sketch than to a running program.
4. **Cleaner database.** The ER step removes repeated data, such as typing a student's name in every loan. Fewer copies mean fewer spelling mistakes. The data stays consistent for years.
5. **Easier testing.** Every requirement with a clear ID becomes a test case with a clear expected result. The tester can prepare test cases while the developers still code. Nothing is left to memory.
6. **Smoother report writing.** The design chapter of the TU report is the diagrams themselves, with a paragraph each. You do not have to reconstruct them from code afterwards. Examiners usually read this chapter first.
7. **Fair division of work.** Modules and tables are visible, so the leader can assign them without overlap. Each developer knows the interface to the others. Integration week then holds fewer surprises.
8. **Confidence in the viva.** A student who drew the diagram can explain the system from the whole to the part. Questions such as "why this table?" or "where does this data go?" are then easy. Memorised code answers cannot do this.

## Formula and fact sheet

- Functional = what; non-functional = how well; both must be testable.
- DFD symbols: entity (rectangle), process (circle), store (open box), flow (arrow). Level 0 = one process.
- ER cardinality: 1:1, 1:N, M:N (M:N becomes an associative table with two foreign keys).
- PK identifies a row; FK points to a PK in another table. 3NF: no repeated or indirectly dependent data.

## Chapter summary

- Requirements are written as testable functional and non-functional statements.
- Use-case diagrams show actors and functions; DFDs show data movement at level 0 and level 1.
- The ER diagram becomes the schema; foreign keys protect the data (a real script proved it).
- Wireframes and a design-first habit save weeks of rework and help in the viva.

## Practice

1. Differentiate functional and non-functional requirements with two examples each.
2. Rewrite "the system should be fast" as a testable requirement.
3. Draw the use-case diagram for an online bus-ticket system with two actors.
4. State four rules for drawing DFDs.
5. What is a context diagram? What does balancing mean?
6. Convert the many-to-many relationship between STUDENT and COURSE into tables.
7. What does the script in Section 3.4 prove with the "rejected" line?
8. Why should the loan table store `member_id` instead of the member's name?
9. List the controls a login screen needs to be secure.
10. A library has 1,200 members and each borrows on average 15 books a year. How many rows does the `issue` table gain per year, and per day (365 days)?

::: note Answers and worked solutions
**1.** Functional: "issue a book", "calculate fine". Non-functional: "respond in 30 s", "store hashed passwords".
**2.** "Every search over 5,000 books returns in under 2 seconds on the college PC."
**3.** Actors: passenger (search, book, cancel), operator (add bus, view sales); boundary box around the use cases.
**4.** Name each flow; a process needs an input and an output; stores connect only to processes; no entity-to-entity or store-to-store flows.
**5.** A level 0 DFD with one process. Balancing: the external flows in level 1 equal those in level 0.
**6.** STUDENT(student_id, ...), COURSE(course_id, ...), ENROLMENT(student_id FK, course_id FK, grade).
**7.** The foreign key stops a loan for member 99, who does not exist, so no orphan records enter the database.
**8.** Names repeat, change and can be misspelt; an ID is unique and stable, and the name is stored only once.
**9.** Hashed and salted passwords, lock-out after repeated failures, masked input, no password in logs or source code.
**10.** 1,200 × 15 = **18,000 rows per year**; 18,000 / 365 ≈ **49 per day**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Differentiate functional and non-functional requirements, with examples.**

*Introduction.* Requirements describe what users need from the system. Writing them clearly before design prevents misunderstanding and gives the tester something to check.

| Point | Functional | Non-functional |
|---|---|---|
| Meaning | what the system does | how well it does it |
| Example (CampusShelf) | F4: fine = Rs 2 × late days | N1: issue in under 30 seconds |
| Described by | features, inputs, outputs | speed, security, usability, reliability |
| Test | does the feature give the right result? | is the measured quality within the limit? |
| If missing | the system lacks a function | the system works but is slow, unsafe or hard to use |

*Writing rules.* Each requirement has an ID, one sentence, the word "shall" and a test (see the table in Section 3.1). Vague words such as "fast" or "user-friendly" are replaced by numbers.

*Conclusion.* Both kinds are needed: a system with every function but a 3-minute response fails N1, and a fast system without fines fails F4.

**Q2 (5 marks). Explain level 0 and level 1 DFD with the symbols used.**

*Introduction.* A data-flow diagram models how data moves through a system, ignoring control logic and code.

*Symbols.* External entity (rectangle): person or system outside, such as the librarian. Process (circle): transforms data, numbered such as 2.0. Data store (open box): data at rest, such as D3 Issues. Data flow (arrow): named data in motion.

*Level 0.* The context diagram shows the whole system as one process with its external entities and flows (Figure 3.2): book, member and issue data in; receipts, fines and overdue lists out.

*Level 1.* The one process splits into three: 1.0 Manage catalogue, 2.0 Issue and return, 3.0 Overdue reports, connected to stores D1, D2 and D3 (Figure 3.3).

*Rules.* Name every flow; every process has input and output; stores connect only to processes; levels must balance.

*Conclusion.* The two levels let the examiner see the system first as a whole, then in parts.

**Q3 (10 marks). Prepare the analysis and design of a library book-issue system: requirements, use cases, DFD, ER diagram and screens.**

*Introduction.* The design phase turns the scope of the project into documents that the team can code from and the examiner can read. For a college library with 1,200 members the work is as follows.

*1. Requirements.* Functional: login (F1), manage books and members (F2), issue for 14 days if a copy exists (F3), fine of Rs 2 per day late on return (F4), overdue list (F5). Non-functional: under 30 seconds per transaction (N1), salted-hash passwords (N2), learnable in 15 minutes (N3). Each has a test (Section 3.1).

*2. Use cases.* Actors: librarian and student. The librarian uses login, manage books, manage members, issue, return and fine, and overdue report; the student searches and views own loans (Figure 3.1).

*3. DFD.* Level 0 has one process with the librarian and student as entities (Figure 3.2). Level 1 has three processes and three data stores (Figure 3.3) and is balanced with level 0.

*4. ER diagram and schema.* Entities MEMBER, BOOK and ISSUE; MEMBER 1:N ISSUE and BOOK 1:N ISSUE, which resolves the many-to-many relationship (Figure 3.4). Primary keys are `member_id`, `book_id` and `issue_id`; ISSUE carries the foreign keys. The tables are in third normal form, and the script of Section 3.4 showed the foreign key rejecting an invalid member.

*5. Screens.* Login, issue and overdue wireframes (Plate 3.1) were reviewed by the librarian before coding.

*6. Traceability.* Each requirement maps to a use case, a process, a table and a screen:

| Requirement | Use case | DFD process | Table | Screen |
|---|---|---|---|---|
| F1 login | Log in | (entry) | librarian (added in Unit 4) | Login |
| F3 issue | Issue book | 2.0 | issue, book | Issue book |
| F4 fine | Return and fine | 2.0 | issue | Issue book |
| F5 overdue | Overdue report | 3.0 | issue, member | Overdue report |

*7. Validation.* Data checks: copies cannot be negative, a loan needs an existing member and book, dates must be valid.

*Conclusion.* With requirements, diagrams, schema and screens agreed with the librarian, coding becomes translation rather than invention. The same documents form the design chapter of the project report.
