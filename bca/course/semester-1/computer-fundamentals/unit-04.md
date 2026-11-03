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

### 4.1.1 Applications of DBMS

1. **Banking and finance.** Banks keep accounts, balances and transactions in a DBMS so that every deposit and withdrawal is recorded exactly once. ConnectIPS, Fonepay and ATM networks read and update these tables within seconds. Transaction control (ACID) makes sure money is never lost half-way between two accounts.
2. **Education.** A university stores student profiles, enrolment, attendance and results in a database. Tribhuvan University's EMIS and college admission portals let staff search thousands of records quickly. Different views let a teacher see marks while an accountant sees fees.
3. **Government services.** The National ID, citizenship, vehicle registration and tax records of Nepal are held in databases. The Nagarik App and the Inland Revenue Department portal fetch data from them for citizens. Central storage avoids repeated forms and duplicated records.
4. **Healthcare.** Hospitals store patient history, prescriptions, test reports and bed use. DHIS2, used by Nepal's Ministry of Health, collects district health data in one database. Doctors can see earlier reports, which improves treatment and avoids repeated tests.
5. **Airlines and travel.** Reservation systems keep flights, seats and passengers in a shared database. Two agents must never sell the same seat, so concurrency control locks the record. Buddha Air and Yeti Airlines booking sites depend on this.
6. **Retail and e-commerce.** Shops keep products, stock, customers and bills in tables. Daraz and local supermarkets use them to find an item, update stock after a sale and print invoices. Reports of best-selling goods help the owner reorder in time.
7. **Telecommunications.** Ncell and Nepal Telecom store subscriber details, call records and recharge history. Billing, SIM registration and balance checks are queries on these tables. Millions of simple updates per day need a fast, reliable DBMS.
8. **Social media and web applications.** Websites store users, posts, messages and likes in databases, often a mix of relational (MySQL, PostgreSQL) and NoSQL (MongoDB, Redis) systems. Every page you open runs several queries. Indexes keep the answers quick even with huge data.

**People:** the **database administrator (DBA)** designs storage, grants access and backs up; **designers** model the data; **application programmers** write programs; **end users** query or use forms (casual, naive and sophisticated users).

```svgfig label="4.1" caption="File-processing system (left): each application owns its files, so data is repeated. DBMS (right): one shared database behind a single manager."
f = Fig(760, 270)
f.text(180, 16, "File-processing system", size=12.5, color=RED, bold=True)
f.text(580, 16, "Database approach", size=12.5, color=TEAL, bold=True)
for i, (a, d) in enumerate([("Admission\nprogram", "admission.dat\nname, address"), ("Exam\nprogram", "exam.dat\nname, address, marks"), ("Library\nprogram", "library.dat\nname, address, books")]):
    y = 36 + i * 76
    f.box(10, y, 100, 52, a, fill=ROSE, stroke=RED, size=10.5, bold=True)
    f.box(210, y, 150, 52, d, fill=SOFT, stroke=RED, size=10)
    f.arrow([(110, y + 26), (210, y + 26)], color=RED)
f.text(180, 262, "Address stored 3 times, so it can disagree", size=10, color=RED, italic=True)
f.line(380, 30, 380, 250, color=SLATE, dash=True)
for i, a in enumerate(["Admission", "Exam", "Library"]):
    y = 36 + i * 76
    f.box(400, y, 90, 52, a + "\nprogram", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
    f.arrow([(490, y + 26), (540, 130 + (i - 1) * 10)], color=NAVY)
f.box(540, 100, 80, 60, "DBMS", fill=SAND, stroke=AMBER, size=13, bold=True)
f.arrow([(620, 130), (650, 130)], color=AMBER, both=True)
f.box(650, 78, 100, 104, "Student DB\n(each fact\nstored once)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(580, 262, "Constraints, security and backup in one place", size=10, color=TEAL, italic=True)
```

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

```svgfig label="4.2" caption="ANSI/SPARC three-level architecture and the two mappings that give data independence."
f = Fig(760, 290)
f.box(180, 14, 400, 52, "EXTERNAL LEVEL: user views\n(Teacher view, Student view, Accounts view)", fill=SAND, stroke=AMBER, size=11.5, bold=True)
f.box(180, 118, 400, 52, "CONCEPTUAL LEVEL: whole database\n(entities, attributes, relations, constraints)", fill=BLUE, stroke=NAVY, size=11.5, bold=True)
f.box(180, 222, 400, 52, "INTERNAL LEVEL: physical storage\n(files, indexes, blocks on HDD/SSD)", fill=MINT, stroke=TEAL, size=11.5, bold=True)
f.arrow([(380, 66), (380, 118)], color=AMBER, both=True, label="external/conceptual mapping", lpos=(500, 92))
f.arrow([(380, 170), (380, 222)], color=TEAL, both=True, label="conceptual/internal mapping", lpos=(500, 196))
f.text(95, 92, "Logical data\nindependence", size=10.5, color=AMBER, bold=True)
f.text(95, 196, "Physical data\nindependence", size=10.5, color=TEAL, bold=True)
f.text(670, 40, "End users,\nprogrammers", size=10, color=SLATE); f.text(670, 144, "DBA,\ndesigners", size=10, color=SLATE); f.text(670, 248, "DBMS,\noperating system", size=10, color=SLATE)
```

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

```svgfig label="4.3" caption="ER diagram for a Nepali college: Student enrols in Course (M:N), Teacher teaches Course (1:N), Department has Student (1:N). Bold circle = key attribute; * = multi-valued."
f = Fig(760, 360)
f.box(30, 150, 110, 50, "STUDENT", fill=BLUE, stroke=NAVY, size=12, bold=True, r=3)
f.box(360, 150, 110, 50, "COURSE", fill=BLUE, stroke=NAVY, size=12, bold=True, r=3)
f.box(620, 150, 110, 50, "TEACHER", fill=BLUE, stroke=NAVY, size=12, bold=True, r=3)
f.box(30, 305, 110, 46, "DEPARTMENT", fill=BLUE, stroke=NAVY, size=11, bold=True, r=3)
f.poly([(200, 175), (250, 148), (300, 175), (250, 202)], fill=SAND, stroke=AMBER, label="enrols", lx=250, ly=175, size=10)
f.poly([(495, 175), (545, 148), (595, 175), (545, 202)], fill=SAND, stroke=AMBER, label="teaches", lx=545, ly=175, size=10)
f.poly([(85, 228), (125, 252), (85, 276), (45, 252)], fill=SAND, stroke=AMBER, label="has", lx=85, ly=252, size=10)
f.line(140, 175, 200, 175); f.line(300, 175, 360, 175); f.line(470, 175, 495, 175); f.line(595, 175, 620, 175)
f.line(85, 200, 85, 228); f.line(85, 276, 85, 305)
f.text(156, 165, "M", size=10.5, bold=True); f.text(342, 165, "N", size=10.5, bold=True)
f.text(484, 165, "N", size=10.5, bold=True); f.text(607, 165, "1", size=10.5, bold=True)
f.text(98, 216, "N", size=10.5, bold=True); f.text(98, 296, "1", size=10.5, bold=True)
for cx, t, k, tx in [(40, "RollNo", True, 85), (105, "Name", False, 85), (170, "Phone*", False, 85), (385, "CourseID", True, 415), (455, "Title", False, 415), (640, "TID", True, 675), (710, "TName", False, 675)]:
    f.circle(cx, 60, 27, fill=BLUE if k else SOFT, stroke=NAVY if k else SLATE, label=t, size=8.5, color=NAVY, bold=k)
    f.line(cx, 87, tx, 150, color=SLATE, sw=1)
f.circle(230, 328, 27, fill=BLUE, stroke=NAVY, label="DeptID", size=8.5, color=NAVY, bold=True)
f.line(203, 328, 140, 328, color=SLATE, sw=1)
f.text(330, 270, "Relational design (see below):\nStudent(RollNo, Name, DeptID)\nCourse(CourseID, Title, TID)\nEnrol(RollNo, CourseID, Grade)", size=10, color=SLATE, anchor="start")
```

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

## Model answers: medium (5 marks) and long (10 marks) questions

### Medium questions (5 marks)

**Q2. What are the problems of the file-based system and how does a DBMS solve them? (5 marks)**

In a **file-processing system** each application keeps its own files (Figure 4.1). A college may store a student's address in the admission file, the exam file and the library file.

1. **Redundancy and inconsistency:** the same data is repeated, so a changed address may be updated in one file only.
2. **Data isolation:** files have different formats, so combining them needs new programs.
3. **No concurrent access control:** two clerks changing one record can overwrite each other.
4. **Weak security:** access cannot be limited to selected fields or users.
5. **Program-data dependence:** if the file layout changes, every program must be rewritten.

A **DBMS** solves these by keeping one shared database: controlled redundancy, constraints for integrity, locking for concurrency, per-user permissions, logs for recovery, and data independence through the three-level architecture.

| Problem | File system | DBMS |
|---|---|---|
| Duplicate data | common | controlled |
| Security | file-level | user and column level |
| Concurrent update | unsafe | transactions and locks |
| Backup | manual copy | log-based recovery |

**Example.** A bank cannot let two ATMs withdraw the same balance twice; a DBMS lock prevents this.

**Q12. Normalise Marks(SID, SName, CID, CTitle, Score) to 3NF. (5 marks)**

**Given.** Primary key (SID, CID). Functional dependencies: SID → SName; CID → CTitle; (SID, CID) → Score.

1. **1NF:** every field is atomic and there are no repeating groups, so the table is already in 1NF. It suffers anomalies: SName repeats for every course (update anomaly), and a new course cannot be added until a student takes it (insertion anomaly).
2. **2NF:** remove partial dependencies on part of the key. SName depends only on SID and CTitle only on CID, so split into **Student(SID, SName)**, **Course(CID, CTitle)** and **Marks(SID, CID, Score)**.
3. **3NF:** check for transitive dependencies between non-key attributes. None remain, because Score depends on the whole key, SName on SID alone and CTitle on CID alone. The design is in **3NF**.

| Table | Key | Non-key attributes |
|---|---|---|
| Student | SID | SName |
| Course | CID | CTitle |
| Marks | (SID, CID) | Score |

**Result.** A student's name and a course title are stored once, and joining the three tables on SID and CID rebuilds the original data without loss.

**Q4. Differentiate primary key, candidate key and foreign key. (5 marks)**

A **key** is an attribute or set of attributes that identifies rows. A **super key** is any set that is unique; a **candidate key** is a minimal super key.

1. **Candidate key:** a minimal attribute set that identifies each row uniquely. In Student(RollNo, Email, Name), both RollNo and Email are candidates.
2. **Primary key:** the candidate chosen to identify rows. It must be unique and **not null** (entity integrity). RollNo is chosen.
3. **Alternate key:** a candidate that is not chosen, such as Email.
4. **Foreign key:** an attribute in one table that refers to the primary key of another table. It may repeat and (if optional) may be null (referential integrity).

| Key | Unique? | Null allowed? | Count per table |
|---|---|---|---|
| Primary | yes | no | one |
| Candidate | yes | no (if chosen) | one or more |
| Foreign | no | yes | zero or more |

**Example.** In Enrol(RollNo, CourseID, Grade), (RollNo, CourseID) is the composite primary key and each part is also a foreign key to Student and Course.

### Long questions (10 marks)

**Q13. Explain the three-level architecture of a DBMS. (10 marks)**

**Introduction.** The **ANSI/SPARC three-level architecture** separates what users see from how data is stored, so that each level can change without breaking the others (Figure 4.2). Its main aim is **data independence**.

1. **External level (view level):** describes the part of the database each user group needs. A teacher view shows marks, an accounts view shows fees. There can be many external schemas.
2. **Conceptual level (logical level):** describes the whole database for the organisation: entities, attributes, relationships and constraints. There is only one conceptual schema, and the DBA works here.
3. **Internal level (physical level):** describes how data is stored: files, blocks, indexes, compression and access paths on HDD or SSD.
4. **External/conceptual mapping:** translates a user view into the conceptual tables. It makes **logical data independence** possible.
5. **Conceptual/internal mapping:** translates tables into storage structures. It makes **physical data independence** possible.
6. **Logical data independence:** the conceptual schema can change (add the column `Email`) without rewriting external views or programs that do not use it.
7. **Physical data independence:** storage can change (add an index, move to SSD) without changing the conceptual schema.
8. **Schema and instance:** the schema is the design at each level; the instance is the data stored at one moment.

| Level | Describes | Users | Changes when |
|---|---|---|---|
| External | user views | end users | user needs change |
| Conceptual | whole database | DBA, designers | business rules change |
| Internal | storage details | DBMS, system | hardware or tuning changes |

**Example.** A college adds a `Phone` column (conceptual change). The library view and its programs still run, which shows logical independence.

**Conclusion.** The three levels give security (users see only their view), flexibility and easier maintenance. Data independence is the main advantage over file systems.

**Q14. Explain entity, attribute, relationship and cardinality with an ER example. (10 marks)**

**Introduction.** The **entity-relationship (ER) model** is a high-level design method that draws the data before any table is created. It uses rectangles for entities, ellipses for attributes and diamonds for relationships (Figure 4.3).

1. **Entity:** a real-world thing about which data is stored, such as Student, Course or Teacher. A **weak entity** has no key of its own and depends on a strong entity (a Dependent of an Employee).
2. **Attribute:** a property of an entity. Types: *simple* (Name), *composite* (Address = ward + municipality), *single-valued* (RollNo), *multi-valued* (Phone), *derived* (Age from DOB) and *key* (RollNo, underlined).
3. **Relationship:** an association between entities, for example Student *enrols in* Course.
4. **Cardinality:** how many instances take part. **1:1** (one citizen, one citizenship number), **1:N** (one department, many students) and **M:N** (many students, many courses).
5. **Participation:** *total* if every instance must take part (every student belongs to a department), *partial* otherwise.
6. **Mapping to tables:** each entity becomes a table; the key of the one side becomes a foreign key on the many side for 1:N; M:N needs a new table.

**College example.** Entities: Student(RollNo, Name, Phone), Course(CourseID, Title), Teacher(TID, TName), Department(DeptID). Relationships: enrols (M:N), teaches (1:N), has (1:N).

| Entity or relationship | Table produced |
|---|---|
| Student | Student(RollNo, Name, DeptID) |
| Course | Course(CourseID, Title, TID) |
| Enrols (M:N) | Enrol(RollNo, CourseID, Grade) |
| Department | Department(DeptID, DName) |

**Conclusion.** ER modelling finds the entities and links early, avoids redundancy and gives a design that converts directly into relational tables.
