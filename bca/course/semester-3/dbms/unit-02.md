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
