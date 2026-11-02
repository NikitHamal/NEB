---
subject: Computer Fundamentals and Applications
grade: BCA Semester 1
unit: 4
title: Database Management System
hours: 8
area: BCA 101 · Computer Fundamentals and Applications · Unit 4
---

Banks, hospitals, schools and online shops are all, at heart, collections of organised data. A **database management system (DBMS)** stores that data once, protects it, and lets many people query and update it at the same time. This unit gives a complete first course in the ideas; the Semester III subject *Database Management System* develops them fully.

::: key What this unit gives you
- Why files were replaced by databases; DBMS advantages and users.
- The three-level architecture and data independence.
- Data models, and the relational model: tables, keys, integrity.
- Entity–relationship (ER) modelling, and a first look at normalisation.
- SQL: creating tables, inserting, querying, joining, grouping, with worked outputs.
:::

## 4.1 Data, database and DBMS

- **Data hierarchy**: bit → byte → **field** → **record** → **file** → **database**.
- A **database** is an organised, shared collection of related data. A **DBMS** is the software that creates, stores, protects and queries it (MySQL, PostgreSQL, Oracle, SQL Server, SQLite). A **database system** = data + DBMS + hardware + users.

**Problems of the file-processing approach:** data redundancy (the same student's address in three files) leading to **inconsistency**; data isolation in different formats; no concurrent access control; weak security; programs depend on file layout.

| Advantage of a DBMS | How |
|---|---|
| Controlled redundancy | one copy, referenced elsewhere |
| Consistency and integrity | constraints enforced centrally |
| Data sharing | many users and applications at once |
| Security | per-user permissions |
| Backup and recovery | logs and restore |
| Data independence | change storage without changing programs |
| Concurrency control | transactions keep simultaneous updates correct |

Disadvantages: cost, complexity, a single point of failure unless replicated.

**People:** the **database administrator (DBA)** designs storage, grants access and backs up; **designers** model the data; **application programmers** write programs; **end users** query or use forms (casual, naive and sophisticated users).

## 4.2 Architecture and data independence

The **three-level (ANSI/SPARC) architecture** separates:

| Level | Describes | Who sees it |
|---|---|---|
| External (view) | the part of the data each user group needs | end users |
| Conceptual (logical) | the whole database: entities, attributes, relations, constraints | DBA, designers |
| Internal (physical) | files, indexes, how bytes lie on disk | system |

- **Logical data independence**: change the conceptual schema (add a column) without rewriting external views/programs.
- **Physical data independence**: change storage (add an index, move to SSD) without changing the conceptual schema.

The **schema** is the design (rarely changes); the **instance** is the data at a moment (changes constantly). **DDL** (data definition language) defines schema; **DML** (data manipulation) queries and updates; **DCL** controls permissions; **TCL** controls transactions.

## 4.3 Data models

A **data model** is a way of describing data and its structure.

- **Hierarchical**: tree, one parent per record (IBM IMS).
- **Network**: graph, many parents allowed (CODASYL).
- **Relational**: data as tables (relations); dominant since the 1980s (Codd, 1970).
- **Object-oriented / document / key-value / graph** (NoSQL): MongoDB, Redis, Neo4j for flexible or huge-scale data.

## 4.4 The relational model

A **relation** is a table. A row is a **tuple** (record), a column is an **attribute** (field); the set of allowed values of an attribute is its **domain**. **Degree** = number of attributes; **cardinality** = number of tuples.

**Keys**

| Key | Meaning |
|---|---|
| Super key | any set of attributes that uniquely identifies a tuple |
| Candidate key | a *minimal* super key |
| Primary key | the candidate key chosen to identify tuples; never NULL |
| Alternate key | a candidate key not chosen |
| Composite key | a key made of more than one attribute |
| Foreign key | attribute(s) that refer to the primary key of another (or the same) table |

**Integrity rules.** *Entity integrity*: a primary key is never NULL. *Referential integrity*: every foreign-key value must match an existing primary-key value (or be NULL). *Domain integrity*: values must fit the attribute's type and constraints.

Example, students and their programmes:

| **Student**: SID (PK) | Name | ProgID (FK) |
|---|---|---|
| 1 | Sita | 10 |
| 2 | Ram | 10 |
| 3 | Hari | 20 |

| **Programme**: ProgID (PK) | PName |
|---|---|
| 10 | BCA |
| 20 | BBS |

`ProgID` in Student is a foreign key to Programme; inserting a student with ProgID 30 breaks referential integrity and is rejected.

## 4.5 Entity–relationship modelling

The **ER model** designs the database before tables are made.

- **Entity**: a thing about which we store data (Student, Course); **weak entity** has no key of its own and depends on another (a Dependent of an Employee).
- **Attribute**: a property: simple/composite, single/multi-valued, stored/derived (Age from DOB). Key attribute is underlined.
- **Relationship**: an association between entities (Student *enrols in* Course). **Cardinality**: 1:1, 1:N, M:N.

ER symbols: rectangle = entity (double = weak), ellipse = attribute, diamond = relationship, lines join them.

**Converting ER to tables:** each entity → a table with its key; a 1:N relationship → put the key of the "one" side as a foreign key on the "many" side; an M:N relationship → a **new table** holding both keys (plus any relationship attribute).

::: example Worked example: M:N enrolment
Student (SID, Name) and Course (CID, Title) are M:N (a student takes many courses; a course has many students). The relational design is: **Student(SID, Name)**, **Course(CID, Title)**, **Enrol(SID, CID, Grade)** with primary key (SID, CID), where SID and CID are also foreign keys.
:::

## 4.6 Normalisation (introduction)

Normalisation removes redundancy and update anomalies by splitting tables. An un-normalised table `Order(OID, Cust, CustPhone, Item)` repeats the phone number on every order line, so changing it means many updates (**update anomaly**), deleting the last order loses the customer (**deletion anomaly**), and a customer cannot be added without an order (**insertion anomaly**).

- **1NF**: every field holds a single atomic value; no repeating groups.
- **2NF**: 1NF and no non-key attribute depends on only *part* of a composite key.
- **3NF**: 2NF and no non-key attribute depends on another non-key attribute (no transitive dependency).

Fix: `Customer(Cust, CustPhone)` and `Order(OID, Cust, Item)`; the phone number is now stored once.

## 4.7 SQL: structured query language

SQL is the standard language of relational databases.

```sql
CREATE TABLE programme (
    prog_id  INT PRIMARY KEY,
    pname    VARCHAR(30) NOT NULL
);
CREATE TABLE student (
    sid      INT PRIMARY KEY,
    name     VARCHAR(40) NOT NULL,
    marks    INT CHECK (marks BETWEEN 0 AND 100),
    prog_id  INT REFERENCES programme(prog_id)
);
INSERT INTO programme VALUES (10, 'BCA'), (20, 'BBS');
INSERT INTO student VALUES (1, 'Sita', 82, 10), (2, 'Ram', 67, 10),
                           (3, 'Hari', 74, 20), (4, 'Gita', 91, 10);
```

Queries on this data:

```sql
SELECT name, marks FROM student WHERE marks >= 75 ORDER BY marks DESC;
```
```output
Gita|91
Sita|82
```

```sql
SELECT p.pname, COUNT(*) AS n, AVG(s.marks) AS avg_marks
FROM student s JOIN programme p ON s.prog_id = p.prog_id
GROUP BY p.pname;
```
```output
BBS|1|74.0
BCA|3|80.0
```

```sql
UPDATE student SET marks = marks + 5 WHERE sid = 2;
DELETE FROM student WHERE marks < 70;
```

The second statement removes nobody here: Ram becomes 72, and everyone else is already ≥ 74.

| Clause | Role |
|---|---|
| `SELECT` | columns (or expressions, aggregates) to return |
| `FROM` | tables; `JOIN … ON` combines tables by matching keys |
| `WHERE` | filters rows *before* grouping |
| `GROUP BY` | one output row per group |
| `HAVING` | filters groups *after* aggregation |
| `ORDER BY` | sort (`ASC` default, `DESC`) |

**Aggregates:** `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`. `LIKE 'S%'` matches names starting with S; `IN (10, 20)`; `IS NULL`; `DISTINCT`. `ALTER TABLE` changes a table, `DROP TABLE` removes it, `GRANT`/`REVOKE` manage permission, `COMMIT`/`ROLLBACK` end a transaction.

**Transactions and ACID.** A transaction (e.g. transfer Rs 500 from A to B) is a unit of work that is **A**tomic (all or nothing), **C**onsistent (rules hold before and after), **I**solated (concurrent transactions do not see each other's half-done work), **D**urable (once committed, it survives a crash).

## Formula and fact sheet

- Data hierarchy: bit → byte → field → record → file → database.
- Three levels: external, conceptual, internal; logical and physical data independence.
- Key hierarchy: super ⊃ candidate ⊃ primary; foreign key links tables.
- Cardinality of a relation = rows; degree = columns.
- M:N needs a third (junction) table; 1:N puts the FK on the many side.
- 1NF atomic; 2NF no partial dependency; 3NF no transitive dependency.
- SQL: WHERE before GROUP BY, HAVING after; ACID for transactions.

## Chapter summary

- A DBMS replaces scattered files with one controlled, shared and secure store.
- The three-level architecture gives data independence.
- Relational databases organise data into tables linked by keys, with integrity rules the DBMS enforces.
- ER modelling designs the database; normalisation removes redundancy and anomalies.
- SQL creates, queries and updates; transactions obey ACID.

## Practice

**A. Short questions**

1. Define database and DBMS. List five advantages of a DBMS.
2. What are the problems of the file-based system?
3. Differentiate schema and instance.
4. Differentiate primary key, candidate key and foreign key.
5. State entity integrity and referential integrity.
6. What is data independence? Name its two types.
7. What are the DDL and DML? Give two commands of each.
8. What does ACID stand for?

**B. Problems** (use the `student` and `programme` tables of §4.7)

9. Write SQL to display names of students of BCA who scored above 70.
10. Write SQL to show the highest mark in each programme.
11. Design tables for a library where one member borrows many books and one book is borrowed by many members over time.
12. Normalise to 3NF: `Marks(SID, SName, CID, CTitle, Score)` with key (SID, CID).

**C. Long questions**

13. Explain the three-level architecture of a DBMS.
14. Explain entity, attribute, relationship and cardinality with an ER example.

::: note Answers and worked solutions
**1.** A database is an organised shared collection of related data; a DBMS is the software that manages it. Advantages: controlled redundancy, consistency, sharing, security, backup/recovery, data independence.
**2.** Redundancy and inconsistency, data isolation, no concurrency control, poor security, program-data dependence.
**3.** Schema is the design of the database; instance is the data stored at a moment.
**4.** Primary key: chosen unique, non-null identifier. Candidate key: any minimal unique attribute set (primary is one of them). Foreign key: refers to a primary key in another table.
**5.** Entity integrity: primary key cannot be NULL. Referential integrity: a foreign key must match an existing primary key or be NULL.
**6.** Ability to change one level without affecting the next higher level. Logical and physical.
**7.** DDL: `CREATE`, `ALTER`, `DROP`. DML: `SELECT`, `INSERT`, `UPDATE`, `DELETE`.
**8.** Atomicity, Consistency, Isolation, Durability.
**9.** `SELECT s.name FROM student s JOIN programme p ON s.prog_id = p.prog_id WHERE p.pname = 'BCA' AND s.marks > 70;`  gives Sita and Gita (Ram has 67).
**10.** `SELECT p.pname, MAX(s.marks) FROM student s JOIN programme p ON s.prog_id = p.prog_id GROUP BY p.pname;`  gives BBS 74, BCA 91.
**11.** Member(MemberID, Name), Book(BookID, Title), Borrow(MemberID, BookID, IssueDate, ReturnDate) with primary key (MemberID, BookID, IssueDate).
**12.** SName depends only on SID and CTitle only on CID (partial dependencies). Split into Student(SID, SName), Course(CID, CTitle), Marks(SID, CID, Score).
**13.** External, conceptual, internal levels with the table of §4.2 and the two independences.
**14.** Use the definitions in §4.5 and draw Student–Enrol–Course as an M:N example.
:::
