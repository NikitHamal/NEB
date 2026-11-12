---
subject: Database Management System
grade: BCA Semester 3
unit: 2
title: Database Design, Architecture and Model
hours: 6
area: BCA 202 · Database Management System · Unit 2
---

This unit shows how a database is *designed* before any table is created: the architecture that hides storage details, the languages used, the data models, and above all the **entity-relationship (E-R) model**.

::: key What this unit gives you
- The design process, three-level architecture and data independence.
- DDL, DML and QBE; the main data models.
- E-R diagrams: entities, attributes, relationships, cardinality, weak entities, generalisation, aggregation.
- Converting an E-R diagram into tables.
:::

## 2.1 The design process and the view of data

Design proceeds in stages: (1) **requirements** gathering; (2) **conceptual design** (E-R diagram, independent of any DBMS); (3) **logical design** (convert to relations of the chosen model, normalise); (4) **physical design** (file organisation, indexes). A **schema** is the description of the database (rarely changes); an **instance** is the data in it at one moment (changes constantly).

## 2.2 Structure of a DBMS and three-level architecture

Components: the **DDL compiler**, **query processor** (parser, optimiser, evaluator), **storage manager** (buffer, file and index manager, transaction and authorisation managers), and the **data dictionary**.

The **ANSI/SPARC three-level architecture** separates:

| Level | Describes | Who sees it |
|---|---|---|
| **External (view)** | the part of the database a user group needs | end users, programmers |
| **Conceptual (logical)** | the whole database: entities, relations, constraints | DBA, designers |
| **Internal (physical)** | files, indexes, blocks, compression | DBMS, DBA |

**Data independence:** *physical* independence means changing the internal level (adding an index) does not change the conceptual schema or programs; *logical* independence means changing the conceptual schema (adding a column) does not break external views. Mappings between levels make this possible.

## 2.3 Database languages

| Language | Purpose | Statements |
|---|---|---|
| **DDL** (data definition) | define and change schema | `CREATE`, `ALTER`, `DROP`, `TRUNCATE` |
| **DML** (data manipulation) | query and change data | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| **DCL** (data control) | permissions | `GRANT`, `REVOKE` |
| **TCL** (transaction control) | transactions | `COMMIT`, `ROLLBACK`, `SAVEPOINT` |

DML is **procedural** (say how) or **declarative/non-procedural** (say what; SQL). **Query By Example (QBE)** is a graphical language where the user fills in skeleton tables with example values, and the system turns them into a query. Example: in a `Student` skeleton, putting `P.` under *name* and `>80` under *marks* means "print names of students with marks over 80".

## 2.4 Data models

| Model | Idea |
|---|---|
| **Hierarchical** | records in a tree; each child has one parent (IBM IMS) |
| **Network** | records in a graph; a child may have many parents (CODASYL) |
| **Relational** | data in tables (relations) linked by values; the dominant model (Unit 3) |
| **Entity-relationship** | entities and relationships for conceptual design |
| **Object-based** | objects with attributes, methods and inheritance; object-relational systems add this to tables |

## 2.5 The entity-relationship model

- **Entity**: a distinguishable thing (a student). **Entity set**: all entities of one type. Drawn as a **rectangle**.
- **Attribute**: a property, drawn as an **ellipse**. Kinds: **simple/composite** (name = first + last), **single/multi-valued** (phone numbers, double ellipse), **stored/derived** (age from date of birth, dashed ellipse), **key attribute** (underlined).
- **Relationship**: an association among entities, drawn as a **diamond**. **Degree** = number of entity sets (binary is most common).
- **Cardinality ratio**: **1:1**, **1:N**, **N:1**, **M:N**. **Participation**: *total* (every entity must take part; double line) or *partial*.
- **Strong entity** has its own key. **Weak entity** has none: it depends on an *owner* entity through an **identifying relationship** (double diamond) and is identified by the owner's key plus its own **partial key**. Example: `Dependent` of `Employee`.

::: example Worked example: college database
Entities: **Department**(dept_id, name), **Student**(sid, name, phone*, dob), **Course**(cid, title, credits). Relationships: Department *offers* Course (1:N, total on Course); Department *has* Student (1:N); Student *enrols in* Course (**M:N**, with attribute `marks`, because the mark belongs to the pair, not to either alone).
:::

### Generalisation, specialisation, aggregation

- **Specialisation** (top-down): split an entity set into sub-groups with extra attributes: `Person` → `Student`, `Teacher` (an **ISA** triangle). **Generalisation** is the same in reverse (bottom-up): combine similar entity sets. Constraints: **disjoint** or **overlapping**; **total** or **partial**. Subclasses inherit the parent's attributes.
- **Aggregation** treats a relationship (with its entities) as a higher-level entity so it can take part in another relationship. Example: `Employee works-on Project` is aggregated, then *Manager monitors* that whole assignment.

## 2.6 Converting an E-R diagram to tables

| E-R construct | Table(s) |
|---|---|
| Strong entity | one table; simple attributes become columns; composite attributes are flattened; key becomes the primary key |
| Multi-valued attribute | separate table (owner key, value); the pair is the key |
| 1:1 relationship | add the key of one side as a foreign key to the other (prefer the total side) |
| 1:N | add the key of the **N** side's partner (the "1" side's key) as a foreign key in the **N** side's table |
| **M:N** | **new table** with both keys (as a composite primary key) plus relationship attributes |
| Weak entity | table with owner's key + partial key as primary key |
| Specialisation | table per subclass with the parent's key (or one table with a type column) |

::: example Worked example: the tables for the college diagram
`department(dept_id PK, name)` · `student(sid PK, name, dob, dept_id FK)` · `student_phone(sid FK, phone, PK(sid, phone))` · `course(cid PK, title, credits, dept_id FK)` · `enrollment(sid FK, cid FK, marks, PK(sid, cid))`. The M:N relationship became `enrollment`; the 1:N relationships became foreign keys; the multi-valued `phone` got its own table.
:::

## 2.7 Seeing the ideas: views, models and diagrams

A library card catalogue is the best everyday picture of a database view. Every book has one physical copy on a shelf but several cards in the cabinet: one filed under the author, one under the title and one under the subject. The reader sees a different arrangement of the same facts, which is exactly what the external level of a DBMS offers.

```photogrid label="2.1" cols="2" ratio="1.1" caption="One book, many views. (a) Drawers of a subject catalogue in a university library: each card is a record, the label on each drawer is an index entry and the cabinet is the access path. (b) The same book as three cards. The facts are stored once on the shelf (the internal level) while the author, title and subject cards (external views) let a reader enter the collection by different routes. A DBMS gives the same freedom: one stored table, many views, and the stored layout can be reorganised without changing what readers see."
@ photo id="bca202/catalog" cap="Subject catalogue drawers, Graz University Library"
fit 1.1
focus 0.5 0.5
call 0.5 0.12 0.45 0.45 "one card = one record"
@ svg cap="Three cards, one book"
f = Fig(300, 270)
cards = [("Author card", "Rai, M.", "Database Systems", TEAL, MINT, 8), ("Title card", "Database Systems", "Rai, M.", NAVY, BLUE, 96), ("Subject card", "Databases", "Database Systems", AMBER, SAND, 184)]
for nm, l1, l2, st, fl, y in cards:
    f.box(10, y, 190, 70, "", fill=fl, stroke=st, sw=1.6)
    f.text(18, y + 14, nm, size=10, color=st, bold=True, anchor="start")
    f.text(18, y + 36, l1, size=11, color=SLATE, bold=True, anchor="start")
    f.text(18, y + 54, l2, size=9.5, color=SLATE, anchor="start")
    f.arrow([(200, y + 35), (240, 135)], color=st, sw=1.4)
f.box(236, 100, 60, 70, "Book on\nshelf\n(stored\nonce)", fill=SOFT, stroke=SLATE, size=9, bold=True)
```

```svgfig label="2.1" caption="The three-level (three-schema) architecture. Each user group sees an external view that contains only the columns it needs. The conceptual schema describes the whole database logically: tables, columns, keys and constraints. The internal schema describes how the data are really stored: files, indexes and block layout. Two mappings connect the levels. A change below a mapping can be absorbed by the mapping so the level above stays the same: physical data independence between the internal and conceptual levels, logical data independence between the conceptual and external levels."
f = Fig(580, 290)
f.box(10, 10, 130, 44, "External view 1\nLibrary: sid, name", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(160, 10, 130, 44, "External view 2\nExam: sid, marks", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(310, 10, 130, 44, "External view 3\nFee: sid, dues", fill=SAND, stroke=AMBER, size=10, bold=True)
f.text(500, 32, "what each\nuser sees", size=10, color=AMBER, bold=True)
for x in (75, 225, 375):
    f.arrow([(x, 54), (x, 96)], color=SLATE, sw=1.3)
f.box(10, 96, 430, 50, "Conceptual schema (logical)\nStudent(sid, name, dob, dept_id), Result(sid, cid, marks),\nFee(sid, dues) + keys and constraints", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.text(500, 120, "what the whole\ndatabase means", size=10, color=NAVY, bold=True)
f.arrow([(225, 146), (225, 186)], color=SLATE, sw=1.3)
f.box(10, 186, 430, 44, "Internal schema (physical)\nheap file, B+ tree index on sid, 8 KB blocks", fill=MINT, stroke=TEAL, size=10, bold=True)
f.text(515, 208, "how it is\nstored", size=10, color=TEAL, bold=True)
f.arrow([(225, 230), (225, 258)], color=SLATE, sw=1.3)
f.box(150, 258, 150, 28, "Disk", fill=SOFT, stroke=SLATE, size=10.5, bold=True)
f.text(450, 76, "logical data\nindependence", size=9, color=RED, bold=True, anchor="start")
f.text(450, 166, "physical data\nindependence", size=9, color=RED, bold=True, anchor="start")
```

```svgfig label="2.2" caption="The college diagram of Section 2.5 drawn out. Rectangles are entity sets, ellipses are attributes (underlined text marks a key attribute), diamonds are relationships, and the labels 1 and N give the cardinality. The enrols-in relationship is many-to-many (M:N) and carries its own attribute, marks, which belongs to the pair of student and course. In the tables of Section 2.6 this diamond becomes the enrollment table with the composite key (sid, cid)."
f = Fig(580, 322)
def ent(x, y, w, nm): f.box(x, y, w, 34, nm, fill=BLUE, stroke=NAVY, size=11, bold=True)
def att(cx, cy, nm, key=False):
    f.raw(f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="13" fill="#ffffff" stroke="{TEAL}" stroke-width="1.3"/>')
    f.text(cx, cy, nm, size=9, color=TEAL, bold=True, vmid=True)
    if key: f.line(cx - 12, cy + 6, cx + 12, cy + 6, color=TEAL, sw=1)
def rel(cx, cy, nm): f.poly([(cx, cy - 22), (cx + 44, cy), (cx, cy + 22), (cx - 44, cy)], fill=SAND, stroke=AMBER, label=nm, lx=cx, ly=cy, size=9.5, color=AMBER)
ent(40, 110, 110, "Department"); ent(235, 238, 110, "Student"); ent(430, 110, 110, "Course")
att(40, 60, "dept_id", True); att(130, 40, "name")
att(310, 290, "sid", True); att(395, 290, "name"); att(235, 290, "dob")
att(470, 60, "cid", True); att(550, 60, "title"); att(530, 160, "credits")
rel(95, 200, "has"); rel(290, 110, "offers"); rel(430, 220, "enrols in")
f.line(40, 73, 80, 110, color=TEAL); f.line(130, 53, 110, 110, color=TEAL)
f.line(235, 277, 270, 272, color=TEAL); f.line(380, 277, 320, 272, color=TEAL); f.line(310, 277, 290, 272, color=TEAL)
f.line(470, 73, 480, 110, color=TEAL); f.line(550, 73, 520, 110, color=TEAL); f.line(530, 147, 510, 144, color=TEAL)
f.line(95, 144, 95, 178, color=NAVY, sw=1.6); f.line(95, 222, 240, 250, color=NAVY, sw=1.6)
f.line(150, 127, 246, 110, color=NAVY, sw=1.6); f.line(334, 110, 430, 127, color=NAVY, sw=1.6)
f.line(345, 255, 386, 225, color=NAVY, sw=1.6); f.line(474, 220, 490, 144, color=NAVY, sw=1.6)
f.text(110, 160, "1", size=10, color=RED, bold=True); f.text(120, 232, "N", size=10, color=RED, bold=True)
f.text(165, 112, "1", size=10, color=RED, bold=True); f.text(405, 112, "N", size=10, color=RED, bold=True)
f.text(375, 232, "M", size=10, color=RED, bold=True); f.text(498, 190, "N", size=10, color=RED, bold=True)
att(500, 262, "marks"); f.line(466, 255, 466, 232, color=TEAL, dash=True)
```

```svgfig label="2.3" caption="Three classic data models, drawn for the same college data. In the hierarchical model records form a tree and each child has exactly one parent, so a course that belongs to two departments must be stored twice. The network model allows a record to have many parents through explicit links (pointers), at the price of difficult navigation. The relational model stores everything in tables and joins them by matching values, which is why SQL does not need to know any physical link."
f = Fig(580, 230)
f.text(95, 14, "Hierarchical (tree)", size=11, color=NAVY, bold=True)
f.box(55, 26, 80, 26, "Dept CS", fill=BLUE, stroke=NAVY, size=10, bold=True)
for i, (nm, x) in enumerate([("Course A", 10), ("Course B", 105)]):
    f.box(x, 100, 80, 26, nm, fill=MINT, stroke=TEAL, size=9.5, bold=True)
    f.arrow([(95, 52), (x + 40, 100)], color=SLATE, sw=1.3)
f.text(95, 150, "one parent only", size=9.5, color=RED, bold=True)
f.text(290, 14, "Network (graph)", size=11, color=NAVY, bold=True)
f.box(215, 26, 70, 26, "Dept CS", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(315, 26, 70, 26, "Dept Mgmt", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(215, 100, 70, 26, "Course A", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(315, 100, 70, 26, "Course B", fill=MINT, stroke=TEAL, size=9.5, bold=True)
for a, b in [((250, 52), (250, 100)), ((250, 52), (350, 100)), ((350, 52), (350, 100)), ((350, 52), (250, 100))]:
    f.arrow([a, b], color=SLATE, sw=1.2)
f.text(300, 150, "many parents via links", size=9.5, color=AMBER, bold=True)
f.text(485, 14, "Relational (tables)", size=11, color=NAVY, bold=True)
rows = [("did", "cid", "title"), ("CS", "A", "DBMS"), ("CS", "B", "Java"), ("MG", "B", "Java")]
for r, row in enumerate(rows):
    for c, v in enumerate(row):
        f.box(430 + c * 48, 28 + r * 26, 48, 26, v, fill=BLUE if r == 0 else SOFT, stroke=NAVY, size=9.5, bold=(r == 0), r=0)
f.text(500, 150, "values link rows", size=9.5, color=TEAL, bold=True)
f.box(10, 178, 560, 40, "Relational won because queries state WHAT is wanted; the DBMS finds HOW. Codd proposed it in 1970 at IBM.", fill=SAND, stroke=AMBER, size=10, bold=True)
```

```svgfig label="2.4" caption="Specialisation and generalisation. Person is the general (super-class) entity set with the attributes common to everyone. Student and Teacher are specialised (sub-class) sets that inherit those attributes and add their own. Read downwards this is specialisation; read upwards it is generalisation. The label d means disjoint (a person is in at most one sub-class); a total constraint would be drawn with a double line."
f = Fig(580, 210)
f.box(200, 8, 180, 50, "Person\nid, name, phone", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.poly([(290, 76), (272, 100), (308, 100)], fill=SAND, stroke=AMBER, label="d", lx=290, ly=94, size=9, color=AMBER)
f.line(290, 58, 290, 76, color=NAVY, sw=1.6)
f.line(290, 100, 290, 106, color=NAVY, sw=1.6); f.line(110, 106, 470, 106, color=NAVY, sw=1.6)
f.line(110, 106, 110, 130, color=NAVY, sw=1.6); f.line(470, 106, 470, 130, color=NAVY, sw=1.6)
f.box(20, 130, 180, 50, "Student\n+ roll_no, program", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(380, 130, 180, 50, "Teacher\n+ salary, designation", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(290, 160, "inherit id, name, phone", size=10, color=SLATE, bold=True)
f.text(290, 196, "specialisation (down)  |  generalisation (up)", size=10, color=RED, bold=True)
```

The hierarchical model is easiest to understand in something you can photograph. When IBM, North American Rockwell and Caterpillar built the Information Management System (IMS) in the 1960s, one of the first jobs was the bill of materials of the Apollo rockets: a rocket is made of stages, a stage of engines and tanks. Every part has exactly one parent, so the data forms a tree. The plate below keeps that bill of materials in a single table and asks a real PostgreSQL server how many parts sit at each level.

```photogrid label="2.2" cols="2" ratio="1.1" caption="The hierarchical model in steel. (a) The Saturn V first stage, second stage and third stage laid out in a hall at the Johnson Space Center. A rocket is a tree of assemblies, which is why IBM's IMS, first written for the Apollo programme, stores records as parent and child segments. (b) The same hierarchy as 14 rows of one table part(pid, name, parent). A recursive query on real PostgreSQL 15 counted 1 part at level 0, 4 at level 1 and 9 at level 2, and 3 parts under the S-IC stage. A part with two parents (a bolt used by two stages) cannot be stored as a tree: that limit led to the network model and then to the relational model."
@ photo id="bca202/saturn" cap="Saturn V stages, Johnson Space Center"
fit 1.1
focus 0.5 0.5
@ svg cap="Bill of materials as a tree (counts from a recursive query)"
tree = {"Saturn V": ["S-IC", "S-II", "S-IVB", "IU"], "S-IC": ["F-1 x5", "RP-1 tank", "LOX tank"], "S-II": ["J-2 x5", "LH2 tank", "LOX tank"], "S-IVB": ["J-2 x1", "LH2 tank"], "IU": ["Computer"]}
lv1 = tree["Saturn V"]
leaves = sum(len(tree[k]) for k in lv1)
assert (1, len(lv1), leaves) == (1, 4, 9) and len(tree["S-IC"]) == 3
f = Fig(300, 262)
f.box(100, 8, 100, 26, "Saturn V", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
for i, k in enumerate(lv1):
    x = 4 + i * 74
    f.line(150, 34, x + 33, 56, color=NAVY, sw=1.3)
    f.box(x, 56, 66, 24, k, fill=BLUE, stroke=NAVY, size=10, bold=True)
    f.line(x + 33, 80, x + 33, 92, color=TEAL, sw=1.2)
    for j, lf in enumerate(tree[k]):
        f.box(x, 92 + j * 28, 66, 22, lf, fill=MINT, stroke=TEAL, size=9.5)
f.text(8, 188, "level 0: 1 part   level 1: 4 parts   level 2: 9 parts", size=10, color=NAVY, bold=True, anchor="start")
f.text(8, 206, "parts under S-IC: 3 (real PostgreSQL 15 run)", size=10, color=TEAL, bold=True, anchor="start")
f.box(8, 218, 284, 36, "one parent per part = tree; a part shared by two\nstages needs two parents, which a tree cannot store", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

### 2.7.1 Eight advantages of the three-level architecture and data independence

1. **Different users get different views.** The library clerk does not need to see marks and the exam officer does not need to see fines. Each external view shows only the columns and rows that a group needs. This keeps screens simple and reports focused.
2. **Security improves.** A view can hide sensitive columns such as salary or password. Users are given permission on the view and never on the base table. A Nepali bank can therefore let a teller see an account balance but not the loan file.
3. **Physical changes do not break programs.** If the DBA adds an index or moves the table to a faster disk, only the internal schema changes. The mapping to the conceptual level absorbs the change. This property is called physical data independence.
4. **Logical changes can be absorbed.** When a new column such as email is added to Student, existing views and programs keep working because they never mention it. Logical data independence is harder to achieve than physical independence, but views make it possible in many cases. Older applications continue to run during an upgrade.
5. **Lower maintenance cost.** Programs depend on a stable logical description, not on file layouts. Rewriting hundreds of programs after every storage change is avoided. Colleges that upgrade their server do not have to rewrite their result software.
6. **One agreed description of the data.** The conceptual schema is the single, shared definition of every table, key and constraint. Everyone in the organisation, from designer to programmer, refers to the same document. Misunderstandings about what a column means become rare.
7. **Easier design and teaching.** Designers can think logically first (E-R diagram, tables) and decide on storage later. A student of Tribhuvan University can learn SQL without knowing anything about disk blocks. The levels divide a complex job into smaller parts.
8. **Better performance tuning.** The DBA can improve speed at the internal level, with indexes, clustering or partitioning, while users keep the same queries. A slow monthly report can be made faster overnight without telling anyone. Tuning and application development proceed independently.

## Formula and fact sheet

- Three levels: external, conceptual, internal; two independences: logical and physical.
- E-R symbols: rectangle (entity), double rectangle (weak), ellipse (attribute), diamond (relationship).
- Tables from E-R: M:N → new table; 1:N → foreign key on the N side; multi-valued → own table.

## Chapter summary

- Design goes requirements → E-R → relations → physical.
- The three-level architecture gives data independence.
- E-R models entities, attributes, relationships, cardinality and participation; extended E-R adds ISA and aggregation.
- Conversion rules turn the diagram into relational tables mechanically.

## Practice

1. Explain the three-level architecture and the two kinds of data independence.
2. Differentiate DDL, DML, DCL and TCL with statements.
3. Define weak entity with an example.
4. Draw an E-R diagram (describe entities, keys, cardinalities) for a library: books, members, loans.
5. Convert it to tables.
6. What are generalisation and aggregation?
7. Distinguish schema and instance.

::: note Answers and worked solutions
**1.** External (user views), conceptual (whole logical schema), internal (storage). Physical independence: storage changes without affecting the conceptual schema; logical independence: conceptual changes without affecting external views/programs.
**2.** DDL defines (CREATE, ALTER, DROP); DML manipulates (SELECT, INSERT, UPDATE, DELETE); DCL controls access (GRANT, REVOKE); TCL controls transactions (COMMIT, ROLLBACK).
**3.** An entity without its own key, identified through an owner: `Dependent(name, age)` of `Employee`.
**4.** Entities: Book(isbn, title), Member(mid, name), Loan as relationship Member *borrows* Book (M:N, attributes issue_date, due_date, return_date).
**5.** `book(isbn PK, title)`, `member(mid PK, name)`, `loan(mid FK, isbn FK, issue_date, due_date, return_date, PK(mid, isbn, issue_date))`: the date joins the key so the same member can borrow the same book twice.
**6.** Generalisation: combine entity sets with common features into a super-class; aggregation: treat a relationship as an entity to relate it to others.
**7.** Schema: the structure (rarely changes). Instance: the data at one moment.
:::

## Model answers (5 and 10 marks)

**Q1 (5 marks). Explain the database languages DDL, DML, DCL and TCL with examples.**

*Introduction.* A DBMS provides several sub-languages, all usually parts of SQL, so that users can define data, use it, protect it and control transactions.

1. **DDL (Data Definition Language).** It defines and changes the structure, that is, the schema. Commands are `CREATE`, `ALTER`, `DROP` and `TRUNCATE`. For example `CREATE TABLE student(sid INT PRIMARY KEY, name VARCHAR(40));` creates a table. The result is stored as metadata in the data dictionary.
2. **DML (Data Manipulation Language).** It retrieves and changes the data inside tables with `SELECT`, `INSERT`, `UPDATE` and `DELETE`. DML is either *procedural*, where the user says how to get the data, or *declarative (non-procedural)*, where the user says only what is wanted, as SQL does. A query such as `SELECT name FROM student WHERE sid = 7;` is declarative DML.
3. **DCL (Data Control Language).** It controls access with `GRANT` and `REVOKE`. For example `GRANT SELECT ON student TO clerk;` lets the user clerk read the table and nothing more.
4. **TCL (Transaction Control Language).** It controls transactions with `COMMIT`, `ROLLBACK` and `SAVEPOINT`. After a group of updates, `COMMIT` makes them permanent and `ROLLBACK` undoes them.

*Example.* In a college system the DBA uses DDL to create the tables, the clerk uses DML to enter marks, the DBA uses DCL to limit the clerk and TCL ensures that a half-entered mark sheet is not saved.

*Conclusion.* Together the four groups cover the whole life of data from definition to safe use.

**Q2 (5 marks). What is data independence? Explain the three-level architecture of a DBMS with a diagram.**

*Introduction.* Data independence is the ability to change the schema at one level without changing the schema at the next higher level. The three-level (ANSI-SPARC) architecture of Figure 2.1 makes this possible.

1. **External level (view level).** It describes the part of the database that one user group sees, for example the library view with sid and name. There can be many external views.
2. **Conceptual level.** It describes the whole database logically: entities, attributes, relationships, keys and constraints, without any storage detail. There is only one conceptual schema.
3. **Internal level (physical level).** It describes how the data are stored: file organisation, indexes, block size and compression.
4. **Mappings.** The external/conceptual mapping and the conceptual/internal mapping translate a request from one level to the next.
5. **Physical data independence.** The storage can be reorganised, for example by adding an index, without altering the conceptual schema or programs.
6. **Logical data independence.** The conceptual schema can be extended, for example by adding a column, without altering existing views or programs.

*Example.* If a college adds an `email` column to Student, the exam view and its programs continue to work unchanged.

*Conclusion.* The three levels separate what users see, what the database means and how it is stored, which reduces maintenance cost.

**Q3 (10 marks). Explain the entity-relationship model. Draw an E-R diagram for a college and convert it into tables.**

*Introduction.* The entity-relationship (E-R) model, proposed by Peter Chen in 1976, describes the real world as entities, attributes and relationships. An E-R diagram is a plan that designers and users can discuss before any table is created. Figure 2.2 shows the college example.

*Components.*
1. **Entity and entity set.** An entity is a distinguishable object such as one student; all students form an entity set, drawn as a rectangle.
2. **Attributes.** Properties drawn as ellipses: simple or composite, single-valued or multi-valued (double ellipse), stored or derived (dashed ellipse), and the key attribute, which is underlined.
3. **Relationship.** An association among entity sets, drawn as a diamond. Its degree is the number of entity sets joined; binary relationships are the most common.
4. **Cardinality.** One-to-one (1:1), one-to-many (1:N), many-to-one and many-to-many (M:N).
5. **Participation.** Total (every entity takes part, a double line) or partial.
6. **Strong and weak entities.** A weak entity such as Dependent has no key of its own and depends on an owner through an identifying relationship (double diamond).
7. **Specialisation, generalisation and aggregation** extend the model with sub-classes and with relationships treated as entities (Figure 2.4).

*The college diagram.* Department offers Course (1:N), Department has Student (1:N), and Student enrols in Course (M:N) with the attribute `marks`.

*Conversion to tables.* Each strong entity becomes a table, 1:N relationships become a foreign key on the N side, and the M:N relationship becomes a new table.

| Table | Columns | Keys |
|---|---|---|
| department | dept_id, name | PK dept_id |
| student | sid, name, dob, dept_id | PK sid; FK dept_id |
| student_phone | sid, phone | PK (sid, phone); FK sid |
| course | cid, title, credits, dept_id | PK cid; FK dept_id |
| enrollment | sid, cid, marks | PK (sid, cid); FK sid, FK cid |

*Conclusion.* The E-R model lets designers capture requirements in a simple picture, and the mapping rules turn that picture into correct relational tables with the right keys.
