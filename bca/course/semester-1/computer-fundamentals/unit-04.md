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

### 4.1.2 Eight advantages of a DBMS

The table above names the benefits in one line each. In an examination answer each of the eight points below should be written with its meaning and an example.

1. **Controlled redundancy.** In a file system the same student address may be stored in the library, accounts and exam files. A DBMS keeps one copy and links to it from other tables. This saves disk space and removes the risk of copies that disagree.
2. **Consistency and integrity.** Rules such as "marks lie between 0 and 100" or "every student belongs to an existing programme" are stored in the database itself. The DBMS refuses data that breaks a rule, whichever program tries to enter it. A college result system therefore cannot hold a mark of 150.
3. **Data sharing.** Many users and applications use the same data at the same time. The accounts section, the exam section and the principal see one up-to-date record of a student. Nepal's EMIS and the National ID system depend on this shared view.
4. **Security.** The DBA gives each user only the permissions needed. A clerk may read fee records but not change marks, while a teacher may enter marks for one course. Passwords, roles and audit logs show who did what.
5. **Backup and recovery.** The DBMS keeps logs of every change, so after a power failure it can restore the last correct state. Banks run backups every night and can replay the log to the exact minute. A file system usually offers only a copy of the files.
6. **Data independence.** Programs do not depend on how data is physically stored. Adding an index or a new column does not force every program to be rewritten. This reduces maintenance cost over the years.
7. **Concurrency control.** When two clerks update the same account at once, locks and transactions keep the result correct. Without them, two airline agents could sell the same seat. The DBMS handles this so that programmers need not.
8. **Faster development and standard access.** SQL, report writers and form builders let a new application be built in days rather than months. The same language works on MySQL, PostgreSQL, Oracle and SQL Server. Data standards also make exchange between organisations easier.

### 4.1.3 Seven disadvantages of a DBMS

1. **High cost.** Commercial systems such as Oracle have expensive licences, and a good server, storage and backup system add more. Small organisations may find the cost too high. Open-source systems such as PostgreSQL reduce, but do not remove, this cost.
2. **Complexity.** Design, normalisation, indexing and tuning need real skill. A badly designed database is slow and hard to change. Teams must invest time in modelling before coding.
3. **Need for trained staff.** A DBA, designers and programmers are required, and they are scarce in many Nepali districts. Their salaries add to running costs. Training for ordinary users is also needed.
4. **Overhead for small tasks.** For a simple list of 50 names, a spreadsheet is faster to set up than a full DBMS. The DBMS uses memory, processor time and disk space even for tiny jobs. It pays off only when data is large or shared.
5. **Single point of failure.** If the central database server stops, every application that depends on it stops. Hospitals and banks therefore replicate the data on a second server. This again increases cost.
6. **Conversion cost.** Moving old paper registers or spreadsheets into a database needs careful cleaning and re-entry. Errors in the old data must be corrected during the move. Municipalities digitising records have found this to be the longest step.
7. **Large damage if security fails.** Because data is concentrated in one place, a successful attack exposes everything. Leaks of customer records have happened in many countries. Strong passwords, encryption, patching and access logs are essential.

```photogrid label="4.1" cols="3" ratio="1.05" caption="From drawers to databases. (a) A card filing cabinet: finding a record means walking along drawers. (b) A library card catalogue: an index sorted by title or author lets you jump to the right drawer. (c) Charles Bachman (1924 to 2017), who designed the first database management system (IDS) at General Electric in the early 1960s and received the Turing Award in 1973."
@ photo id="bca101/filecab" cap="File storage: one drawer per name, each program has its own cabinet"
fit 1.05
focus 0.5 0.5
@ photo id="bca101/cardcat" cap="Index: the sorted card catalogue is the ancestor of a database index"
fit 1.05
focus 0.5 0.55
@ photo id="bca101/bachman" cap="Charles Bachman: inventor of the first DBMS"
fit 1.05
focus 0.5 0.7
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

```svgfig label="4.4" caption="Normalisation with real data, run in SQLite. A Marks table with 7 rows repeats the course title 7 times and the student name 7 times. Renaming course 101 must touch 3 rows before normalisation but 1 row after it. The three normalised tables join back to exactly the original 7 rows."
import sqlite3
rows = [(1, "Sita", 101, "Database", 82), (1, "Sita", 102, "Networks", 77), (2, "Ram", 101, "Database", 67), (2, "Ram", 103, "C Programming", 71), (3, "Hari", 102, "Networks", 74), (3, "Hari", 103, "C Programming", 88), (4, "Gita", 101, "Database", 91)]
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE marks(sid, sname, cid, ctitle, score)")
db.executemany("INSERT INTO marks VALUES (?,?,?,?,?)", rows)
title_copies = db.execute("SELECT COUNT(ctitle) FROM marks").fetchone()[0]
name_copies = db.execute("SELECT COUNT(sname) FROM marks").fetchone()[0]
db.execute("CREATE TABLE student AS SELECT DISTINCT sid, sname FROM marks")
db.execute("CREATE TABLE course AS SELECT DISTINCT cid, ctitle FROM marks")
db.execute("CREATE TABLE result AS SELECT sid, cid, score FROM marks")
ns = db.execute("SELECT COUNT(*) FROM student").fetchone()[0]
nc = db.execute("SELECT COUNT(*) FROM course").fetchone()[0]
nr = db.execute("SELECT COUNT(*) FROM result").fetchone()[0]
back = db.execute("SELECT COUNT(*) FROM (SELECT r.sid, s.sname, r.cid, c.ctitle, r.score FROM result r JOIN student s USING(sid) JOIN course c USING(cid) EXCEPT SELECT * FROM marks)").fetchone()[0]
upd_before = db.execute("UPDATE marks SET ctitle = 'DBMS' WHERE cid = 101").rowcount
upd_after = db.execute("UPDATE course SET ctitle = 'DBMS' WHERE cid = 101").rowcount
assert (title_copies, name_copies, ns, nc, nr, back, upd_before, upd_after) == (7, 7, 4, 3, 7, 0, 3, 1)
f = Fig(760, 330)
f.box(8, 8, 330, 28, "Un-normalised: Marks(SID, SName, CID, CTitle, Score)", fill=ROSE, stroke=RED, size=10.5, bold=True)
hdr = ["SID", "SName", "CID", "CTitle", "Score"]; wd = [34, 52, 36, 112, 46]
x0 = 8
for j, h in enumerate(hdr):
    f.box(x0, 42, wd[j], 22, h, fill=BLUE, stroke=NAVY, size=9.5, bold=True); x0 += wd[j]
for i, r in enumerate(rows):
    x0 = 8
    for j, v in enumerate(r):
        hot = (j == 3 and r[2] == 101)
        f.box(x0, 66 + i * 24, wd[j], 22, str(v), fill=(SAND if hot else SOFT), stroke=(AMBER if hot else SLATE), size=9.5); x0 += wd[j]
f.text(8, 250, f"CTitle stored {title_copies} times, SName {name_copies} times", size=10.5, color=RED, bold=True, anchor="start")
f.text(8, 270, f"Rename course 101: {upd_before} rows to change (miss one = inconsistency)", size=10.5, color=SLATE, anchor="start")
f.arrow([(345, 150), (385, 150)], color=TEAL, sw=2.2)
f.text(365, 136, "3NF", size=10.5, color=TEAL, bold=True)
f.box(395, 8, 357, 28, "3NF: three tables, each fact stored once", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(395, 46, 112, 20, f"Student ({ns} rows)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
for i, (a, b) in enumerate([(1, "Sita"), (2, "Ram"), (3, "Hari"), (4, "Gita")]):
    f.box(395, 68 + i * 22, 36, 20, str(a), fill=SOFT, stroke=SLATE, size=9.5); f.box(431, 68 + i * 22, 76, 20, b, fill=SOFT, stroke=SLATE, size=9.5)
f.box(520, 46, 232, 20, f"Course ({nc} rows)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
for i, (a, b) in enumerate([(101, "DBMS"), (102, "Networks"), (103, "C Programming")]):
    f.box(520, 68 + i * 22, 44, 20, str(a), fill=SOFT, stroke=(AMBER if a == 101 else SLATE), size=9.5); f.box(564, 68 + i * 22, 188, 20, b, fill=(SAND if a == 101 else SOFT), stroke=(AMBER if a == 101 else SLATE), size=9.5)
f.box(395, 168, 357, 20, f"Result ({nr} rows): SID, CID, Score (key = SID + CID)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
for i, r in enumerate(rows):
    f.box(395 + i * 51, 190, 49, 22, f"{r[0]},{r[2]},{r[4]}", fill=SOFT, stroke=SLATE, size=8.5)
f.text(395, 240, f"Rename course 101: {upd_after} row to change", size=10.5, color=TEAL, bold=True, anchor="start")
f.text(395, 260, f"Join of the three tables minus original Marks = {back} rows (lossless)", size=10.5, color=SLATE, anchor="start")
f.text(395, 288, "2NF removed SName (depends on SID only) and CTitle (CID only).", size=10, color=SLATE, anchor="start")
f.text(395, 306, "No transitive dependency remains, so the tables are in 3NF.", size=10, color=SLATE, anchor="start")
```

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

### 4.7.1 Eight things SQL can do

1. **Define structure (DDL).** `CREATE TABLE`, `ALTER TABLE` and `DROP TABLE` build and change the design. A college can add a `phone` column without losing data. The same commands work on most database systems.
2. **Change data (DML).** `INSERT`, `UPDATE` and `DELETE` add, correct and remove rows. A teacher's mark entry is an `INSERT`, and a correction after rechecking is an `UPDATE`. The `WHERE` clause limits the change to chosen rows.
3. **Ask questions (SELECT).** `SELECT` with `WHERE` and `ORDER BY` returns exactly the rows wanted, sorted as needed. "Students with marks of at least 75, highest first" is one line. The user says what is needed, not how to find it.
4. **Summarise.** `COUNT`, `SUM`, `AVG`, `MIN` and `MAX` with `GROUP BY` and `HAVING` produce totals and averages per group. A municipality can count households per ward in one query. `HAVING` filters groups, while `WHERE` filters rows.
5. **Join tables.** `JOIN ... ON` combines rows from several tables through a key. The student table and the programme table are linked by `prog_id` to show the programme name beside each student. Because data is normalised, joins put it back together.
6. **Enforce rules (constraints).** `PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK` and `FOREIGN KEY` keep data valid. A `CHECK (marks BETWEEN 0 AND 100)` rejects a bad value at entry. Constraints protect integrity for every program that uses the table.
7. **Control access (DCL).** `GRANT` and `REVOKE` give or take away permissions for users and roles. The accounts clerk may `SELECT` fee data, but only the examination head may `UPDATE` marks. This is how a DBMS keeps data secure.
8. **Group work safely (transactions and views).** `COMMIT` and `ROLLBACK` make several changes succeed or fail together, and a `VIEW` stores a query as a virtual table. A fund transfer is committed only when both the debit and the credit are done. Views let a user see only the columns allowed.

```svgfig label="4.5" caption="Why an index matters, measured in code on a table of 100,000 students. The query plan comes from SQLite itself: before the index it scans the whole table; after CREATE INDEX it searches. To find roll number 73,519 a linear scan makes 73,519 comparisons, while binary search over the sorted index makes at most 17 (log2 100,000 is about 16.6)."
import sqlite3, math
N = 100_000
db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE s(roll INTEGER, name TEXT)")
db.executemany("INSERT INTO s VALUES (?,?)", ((i, "S%d" % i) for i in range(1, N + 1)))
q = "SELECT name FROM s WHERE roll = 73519"
plan1 = db.execute("EXPLAIN QUERY PLAN " + q).fetchall()[0][-1]
db.execute("CREATE INDEX idx_roll ON s(roll)")
plan2 = db.execute("EXPLAIN QUERY PLAN " + q).fetchall()[0][-1]
assert plan1.startswith("SCAN") and plan2.startswith("SEARCH") and "idx_roll" in plan2
keys = list(range(1, N + 1)); target = 73519
lin = keys.index(target) + 1
lo, hi, cmp_ = 0, N - 1, 0
while lo <= hi:
    mid = (lo + hi) // 2; cmp_ += 1
    if keys[mid] == target: break
    if keys[mid] < target: lo = mid + 1
    else: hi = mid - 1
assert lin == 73519 and cmp_ <= math.ceil(math.log2(N)) == 17
f = Fig(760, 230)
f.text(10, 16, "Find roll number 73,519 among 100,000 rows", size=11.5, color=NAVY, bold=True, anchor="start")
f.text(10, 62, "no index", size=11, color=RED, bold=True, anchor="start", vmid=True)
f.box(110, 48, 560, 28, "", fill=ROSE, stroke=RED)
f.text(120, 62, f"{lin:,} comparisons   ({plan1})", size=10.5, color=RED, bold=True, anchor="start", vmid=True)
f.text(10, 112, "with index", size=11, color=TEAL, bold=True, anchor="start", vmid=True)
f.box(110, 98, max(8, cmp_ / lin * 560), 28, "", fill=MINT, stroke=TEAL)
f.text(130, 112, f"{cmp_} comparisons   ({plan2})", size=10.5, color=TEAL, bold=True, anchor="start", vmid=True)
f.box(10, 148, 740, 66, f"{lin / cmp_:,.0f} times fewer comparisons.  An index is a sorted copy of one column with pointers to rows,\nlike the library card catalogue of Plate 4.1. The cost: extra disk space, and every INSERT must also update the index.", fill=SOFT, stroke=SLATE, size=10.5)
```

```svgfig label="4.6" caption="The logical order in which SQL works, with real row counts from SQLite on the four-student table of section 4.7. Query: average marks of each programme for students with at least 70 marks, keeping only programmes whose average exceeds 80. FROM/JOIN gives 4 rows, WHERE keeps 3, GROUP BY makes 2 groups, HAVING keeps 1, and ORDER BY sorts that one."
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""CREATE TABLE programme(prog_id INT PRIMARY KEY, pname TEXT);
CREATE TABLE student(sid INT PRIMARY KEY, name TEXT, marks INT, prog_id INT);
INSERT INTO programme VALUES (10,'BCA'),(20,'BBS');
INSERT INTO student VALUES (1,'Sita',82,10),(2,'Ram',67,10),(3,'Hari',74,20),(4,'Gita',91,10);""")
n_join = db.execute("SELECT COUNT(*) FROM student s JOIN programme p ON s.prog_id=p.prog_id").fetchone()[0]
n_where = db.execute("SELECT COUNT(*) FROM student s JOIN programme p ON s.prog_id=p.prog_id WHERE s.marks>=70").fetchone()[0]
groups = db.execute("SELECT p.pname, AVG(s.marks) FROM student s JOIN programme p ON s.prog_id=p.prog_id WHERE s.marks>=70 GROUP BY p.pname ORDER BY p.pname").fetchall()
final = db.execute("SELECT p.pname, AVG(s.marks) FROM student s JOIN programme p ON s.prog_id=p.prog_id WHERE s.marks>=70 GROUP BY p.pname HAVING AVG(s.marks)>80 ORDER BY p.pname").fetchall()
assert (n_join, n_where, len(groups), len(final)) == (4, 3, 2, 1) and groups == [("BBS", 74.0), ("BCA", 86.5)] and final == [("BCA", 86.5)]
f = Fig(760, 250)
f.text(10, 16, "SELECT p.pname, AVG(s.marks) FROM student s JOIN programme p ON s.prog_id = p.prog_id", size=10.5, color=NAVY, bold=True, anchor="start")
f.text(10, 34, "WHERE s.marks >= 70 GROUP BY p.pname HAVING AVG(s.marks) > 80 ORDER BY p.pname;", size=10.5, color=NAVY, bold=True, anchor="start")
steps = [("1 FROM / JOIN", f"{n_join} rows", "all students\nwith programme", BLUE, NAVY), ("2 WHERE", f"{n_where} rows", "Ram (67) is\nremoved", SAND, AMBER), ("3 GROUP BY", f"{len(groups)} groups", "BBS 74.0\nBCA 86.5", MINT, TEAL), ("4 HAVING", f"{len(final)} group", "BBS removed\n(74 is not > 80)", ROSE, RED), ("5 SELECT / ORDER", "1 row", "BCA | 86.5", SOFT, SLATE)]
for i, (t, c, d, bg, st) in enumerate(steps):
    x = 8 + i * 150
    f.box(x, 56, 134, 34, t, fill=bg, stroke=st, size=10.5, bold=True)
    f.box(x, 98, 134, 34, c, fill="#ffffff", stroke=st, size=13, bold=True)
    f.box(x, 140, 134, 50, d, fill="#ffffff", stroke=st, size=10, color=SLATE)
    if i: f.arrow([(x - 16, 73), (x, 73)], color=SLATE)
f.text(380, 214, "WHERE filters rows before grouping; HAVING filters groups after grouping.", size=11, color=SLATE, bold=True)
f.text(380, 236, "This is why an aggregate such as AVG() can appear in HAVING but not in WHERE.", size=10.5, color=SLATE)
```

```photogrid label="4.2" cols="2" ratio="1.15" caption="Where a database really lives, and what keeps it correct. (a) Rows of server cabinets in a data centre, where a bank's database runs on replicated servers. (b) A funds transfer run in SQLite: a rule violation or a crash in the middle makes the whole transaction roll back, so the total never changes (Atomicity and Consistency of ACID)."
@ photo id="bca101/datacenter" cap="Data centre aisle: database servers with replicas for recovery"
fit 1.15
focus 0.5 0.5
@ svg cap="Rs 500 transfer: commit, rule violation and crash"
import sqlite3
def fresh():
    db = sqlite3.connect(":memory:", isolation_level=None)
    db.execute("CREATE TABLE acct(name TEXT PRIMARY KEY, bal INT CHECK (bal >= 0))")
    db.execute("INSERT INTO acct VALUES ('A', 1000), ('B', 500)")
    return db
def bal(db): return dict(db.execute("SELECT name, bal FROM acct").fetchall())
def transfer(db, amt, crash=False):
    db.execute("BEGIN")
    try:
        db.execute("UPDATE acct SET bal = bal - ? WHERE name = 'A'", (amt,))
        if crash: raise RuntimeError("power failure")
        db.execute("UPDATE acct SET bal = bal + ? WHERE name = 'B'", (amt,))
        db.execute("COMMIT"); return "COMMIT"
    except Exception:
        db.execute("ROLLBACK"); return "ROLLBACK"
d1 = fresh(); r1 = transfer(d1, 500); b1 = bal(d1)
d2 = fresh(); r2 = transfer(d2, 1500); b2 = bal(d2)
d3 = fresh(); r3 = transfer(d3, 500, crash=True); b3 = bal(d3)
assert (r1, b1) == ("COMMIT", {"A": 500, "B": 1000}) and (r2, b2) == ("ROLLBACK", {"A": 1000, "B": 500}) and (r3, b3) == ("ROLLBACK", {"A": 1000, "B": 500})
assert all(sum(b.values()) == 1500 for b in (b1, b2, b3))
f = Fig(400, 290)
f.text(10, 16, "Start: A = 1000, B = 500 (total 1,500)", size=11, color=NAVY, bold=True, anchor="start")
cases = [("1. Move Rs 500", r1, b1, MINT, TEAL), ("2. Move Rs 1,500 (A cannot pay)", r2, b2, ROSE, RED), ("3. Crash after the debit", r3, b3, ROSE, RED)]
for i, (t, r, b, bg, st) in enumerate(cases):
    y = 30 + i * 84
    f.box(10, y, 380, 74, "", fill=bg, stroke=st)
    f.text(20, y + 16, t, size=11, color=st, bold=True, anchor="start")
    f.text(20, y + 38, f"result: {r}", size=11, color=SLATE, bold=True, anchor="start")
    f.text(20, y + 58, f"A = {b['A']:,}, B = {b['B']:,}, total {sum(b.values()):,}", size=10.5, color=SLATE, anchor="start")
```

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
15. Explain the advantages and disadvantages of a DBMS and compare it with the file-processing system.
16. What is normalisation? Explain 1NF, 2NF and 3NF with an example.
17. What is a transaction? Explain the ACID properties with an example (5 marks).

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
**15.** Advantages: controlled redundancy, integrity, sharing, security, recovery, independence, concurrency control, fast development. Disadvantages: cost, complexity, skilled staff, overhead, single point of failure, conversion, large breach. Full model answer below.
**16.** Normalisation splits tables to remove anomalies: 1NF atomic values, 2NF no partial dependency, 3NF no transitive dependency. Worked on `Marks` in Figure 4.4; model answer below.
**17.** Atomicity, Consistency, Isolation, Durability; a Rs 500 transfer is committed or rolled back as a whole (Plate 4.2). Model answer in the 5-mark section.
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

**Q17. What is a transaction? Explain the ACID properties with an example. (5 marks)**

A **transaction** is a group of database operations that must be treated as one unit of work: either all of it happens or none of it does. Transferring Rs 500 from account A to account B is one transaction made of two updates, a debit of A and a credit of B. Plate 4.2 shows this run in a real database.

1. **Atomicity:** all steps are done or none is. If the system crashes after the debit but before the credit, the DBMS rolls the debit back (case 3 of Plate 4.2: A = 1,000 and B = 500 again).
2. **Consistency:** a transaction takes the database from one valid state to another. A rule such as `balance >= 0` is never broken; a transfer of Rs 1,500 from an account holding Rs 1,000 is refused and rolled back (case 2).
3. **Isolation:** transactions that run at the same time do not see each other's half-finished work. Two clerks updating the same balance are made to wait for each other by locks.
4. **Durability:** after `COMMIT` the change survives power failure, because it is written to the log on disk.

| Property | Question it answers | Mechanism |
|---|---|---|
| Atomicity | all or nothing? | rollback, log |
| Consistency | rules still true? | constraints |
| Isolation | do users interfere? | locks, versions |
| Durability | is it permanent? | write-ahead log, backup |

**Commands.** `BEGIN` starts the transaction, `COMMIT` makes it permanent and `ROLLBACK` cancels it. In the run of Plate 4.2 the total of the two accounts stays Rs 1,500 in all three cases, which is exactly what ACID promises.

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

**Q15. Explain the advantages and disadvantages of a DBMS and compare it with the file-processing system. (10 marks)**

**Introduction.** A **database management system (DBMS)** is software that creates, stores, protects and queries a shared collection of related data. Before DBMS, every application kept its own files, which caused repeated data and many errors. Banks, hospitals, Tribhuvan University and the National ID system now depend on databases (Plate 4.1 shows the old filing idea and the index idea behind it).

**Problems of the file-processing system.** The same student address is stored in several files (**redundancy**), so a change in one file leaves the others wrong (**inconsistency**). Data sits in different formats (**isolation**), programs depend on the file layout, two users cannot safely update together, and security is weak.

**Advantages of a DBMS**

1. **Controlled redundancy:** one copy of each fact, referenced from other tables.
2. **Consistency and integrity:** rules such as marks from 0 to 100 are enforced centrally.
3. **Data sharing:** many users and applications use the same current data.
4. **Security:** per-user permissions through `GRANT` and `REVOKE`.
5. **Backup and recovery:** logs restore the database after a failure.
6. **Data independence:** storage can change without changing programs.
7. **Concurrency control:** locks and transactions keep simultaneous updates correct.
8. **Fast development:** SQL, forms and reports shorten the time to build an application.

**Disadvantages of a DBMS**

1. High cost of software, hardware and backup.
2. Design and tuning are complex.
3. Skilled staff such as a DBA are needed.
4. Overhead is too heavy for very small jobs.
5. The server is a single point of failure unless it is replicated.
6. Converting old records is slow and costly.
7. A security breach exposes all the data at once.

| Basis | File-processing system | DBMS |
|---|---|---|
| Redundancy | high | controlled |
| Consistency | often lost | enforced by constraints |
| Sharing | difficult | easy |
| Security | weak, file level | per user and per table |
| Concurrent access | unsafe | transactions and locks |
| Data independence | none | logical and physical |
| Cost | low | higher |

**Example.** In a college, the fees office, library and examination section each keep student data. After moving to one database, a change of a student's phone number is made once and every section sees it. Figure 4.5 shows that an index makes one lookup among 100,000 rows need at most 17 comparisons instead of tens of thousands.

**Conclusion.** A DBMS gives accurate, shared and secure data at the price of cost and complexity. For any organisation with large or shared data, the advantages clearly outweigh the disadvantages.

**Q16. What is normalisation? Explain 1NF, 2NF and 3NF with an example. (10 marks)**

**Introduction.** **Normalisation** is the process of organising the tables of a relational database to remove redundancy and the update, insertion and deletion anomalies it causes. It works by splitting a large table into smaller tables joined by keys, guided by **functional dependencies**.

**Example table.** `Marks(SID, SName, CID, CTitle, Score)` with composite key (SID, CID), holding 7 rows for 4 students and 3 courses (Figure 4.4). The course title is repeated 7 times and the student name 7 times.

**Anomalies.** *Update:* renaming course 101 means changing 3 rows; missing one leaves two titles. *Insertion:* a new course cannot be stored until a student takes it. *Deletion:* deleting the only student of a course also deletes the course title.

**Normal forms**

1. **First normal form (1NF):** every field holds one atomic value and there are no repeating groups. A cell such as "Database, Networks" must be split into separate rows. `Marks` is already in 1NF.
2. **Second normal form (2NF):** the table is in 1NF and no non-key attribute depends on only part of a composite key. SName depends on SID alone and CTitle on CID alone, so these partial dependencies are removed: `Student(SID, SName)`, `Course(CID, CTitle)`, `Result(SID, CID, Score)`.
3. **Third normal form (3NF):** the table is in 2NF and no non-key attribute depends on another non-key attribute (no transitive dependency). If `Student` also held `DeptID` and `DeptName`, DeptName would depend on DeptID and must move to a `Department` table. The three tables above are already in 3NF.

| Normal form | Condition | Removes |
|---|---|---|
| 1NF | atomic values, no repeating groups | multi-valued cells |
| 2NF | 1NF and no partial dependency | repetition caused by part of a key |
| 3NF | 2NF and no transitive dependency | non-key depends on non-key |

**Result.** In the run of Figure 4.4 the renaming of course 101 now changes 1 row instead of 3, and joining the three tables returns exactly the original 7 rows, so no information is lost (a **lossless join**).

**Conclusion.** Normalisation gives tables in which each fact is stored once, which saves space and prevents inconsistency. Too much splitting can slow queries because of extra joins, so designers sometimes keep a little redundancy on purpose (denormalisation) for speed.
