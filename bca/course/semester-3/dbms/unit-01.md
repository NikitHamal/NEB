---
subject: Database Management System
grade: BCA Semester 3
unit: 1
title: Introduction to DBMS
hours: 3
area: BCA 202 · Database Management System · Unit 1
---

A **database** is an organised collection of related data; a **Database Management System (DBMS)** is the software that creates, stores, protects and queries it. Banks, railways, hospitals, e-commerce sites and the NEBians app itself all sit on a DBMS.

::: key What this unit gives you
- Definitions: data, information, database, DBMS, and the file-system problems a DBMS solves.
- Objectives, importance, merits, demerits and applications of DBMS.
- The people who use a database system.
:::

## 1.1 Data, information, database and DBMS

**Data** are raw facts (`Sita`, `87`, `2082-04-12`). **Information** is data processed so it is meaningful ("Sita scored 87, the highest mark in BCA 3rd semester"). A **database** stores related data about one enterprise (students, courses, results). A **DBMS** is the program (Oracle, MySQL, PostgreSQL, SQL Server, SQLite) that sits between users and the stored data. A **database system** = data + DBMS + application programs + users + hardware.

**Metadata** is data about data: table names, column types, constraints. It is kept in the **data dictionary** (system catalog).

## 1.2 Why not plain files? Objectives of a DBMS

Before DBMSs, each application kept its own files. The problems were:

| File-system problem | DBMS objective that solves it |
|---|---|
| **Redundancy and inconsistency**: the same address stored in several files, edited in only one | **Controlled redundancy**; one copy, many views |
| **Difficult access**: a new question needs a new program | **Query language** (SQL) answers ad-hoc questions |
| **Data isolation**: many formats in many files | One **data model** and catalog |
| **Integrity problems**: rules (marks 0–100) buried in program code | **Integrity constraints** declared once |
| **Atomicity problems**: a crash halfway through a transfer | **Transactions** with all-or-nothing recovery |
| **Concurrent-access anomalies**: two clerks update one balance | **Concurrency control** |
| **Security problems**: all-or-nothing file access | **Fine-grained authorisation** per user and object |
| **Program–data dependence**: changing a field breaks programs | **Data independence** (Unit 2) |

## 1.3 Importance, merits and demerits

**Merits:** reduced redundancy and inconsistency; shared data; integrity enforced centrally; security and access control; backup and recovery; data independence; standards enforced; faster application development; support for many concurrent users.

**Demerits:** high cost of software, hardware and trained staff; complexity; larger storage and processing overhead; the DBMS is a single point of failure unless replicated; conversion from old file systems is expensive; overkill for a tiny single-user job (a small spreadsheet or file is enough).

## 1.4 Applications of DBMS

Banking (accounts, transactions); airlines and railways (reservations); universities (registration, results); telecom (call records, billing); sales and e-commerce (orders, inventory); human resources (payroll); healthcare (patient records); social media (profiles, posts); government (citizenship, voter and tax records); manufacturing (supply chain).

## 1.5 People in a database system

| Role | Work |
|---|---|
| **Database Administrator (DBA)** | designs the physical database, grants access, backup/recovery, tuning, security (Unit 8) |
| **Database designer** | decides what data to store and designs the schema |
| **Application programmer** | writes programs that use SQL |
| **Sophisticated user / analyst** | writes queries directly, builds reports |
| **Naive (end) user** | uses forms and apps (a bank clerk, an online shopper) |

::: example Worked example: one problem, two answers
A college keeps student address in the *library file*, the *exam file* and the *fee file*. Sita moves; the exam office updates her address, the others do not. A printed admit card goes to the old address: **inconsistency**. With a DBMS, `Student(sid, name, address)` holds the address once; library, exam and fee applications read the same row, so one `UPDATE` fixes all of them.
:::

## 1.6 Seeing the ideas: pictures, figures and the eight-point lists

The story of the DBMS is the story of storage getting faster and data getting shared. Plate 1.1 shows three steps of that story, and Plate 1.2 shows two places where an ordinary Nepali student meets a database almost every week.

```photogrid label="1.1" cols="3" ratio="1.0" caption="From reels to a shared database. (a) Reels of magnetic tape on shelves. In the file-processing era each application owned its own files, usually on tape, and a tape could only be read in order from start to end. (b) The IBM 350 RAMAC disk unit of 1956, the first disk drive: about fifty 24-inch platters stored roughly five million characters and, for the first time, any record could be reached directly without winding a tape. (c) Charles Bachman, who designed the Integrated Data Store (IDS) at General Electric in the early 1960s, one of the first database management systems; he received the Turing Award in 1973."
@ photo id="bca202/nlmtape" cap="Tape reels on shelves"
fit 1.0
focus 0.55 0.5
call 0.5 0.10 0.60 0.30 "one reel = one file"
@ photo id="bca202/ramac" cap="IBM 350 RAMAC disk unit"
fit 1.0
focus 0.6 0.55
call 0.5 0.92 0.60 0.70 "stack of platters"
@ photo id="bca202/bachman" cap="Charles Bachman"
fit 1.0
focus 0.55 0.62
```

```photogrid label="1.2" cols="2" ratio="1.25" caption="Databases at work in everyday life. (a) A railway booking office: every seat sold at a counter must update one shared seat table at once, otherwise two passengers could receive the same seat. (b) A bank ATM: the screen is only the visible end of a database transaction that checks the balance, reduces it and records the withdrawal. The same pattern lies behind a Nepali ConnectIPS transfer, a Fonepay payment or a ticket booked for a flight from Tribhuvan International Airport."
@ photo id="bca202/booking" cap="Reservation counter at a railway station"
fit 1.25
focus 0.5 0.5
call 0.5 0.12 0.50 0.50 "one shared seat table"
@ photo id="bca202/atm" cap="Bank ATM touch screen"
fit 1.25
focus 0.5 0.5
```

```svgfig label="1.1" caption="The same student address kept in three separate files (left) and once in a shared database (right). Under file processing Sita's new address is changed only in the exam file, so the library and fee files now disagree: this is data redundancy leading to data inconsistency. A DBMS keeps one copy of the address in the Student table, and library, exam and fee programs all read that one copy."
f = Fig(580, 250)
f.text(145, 14, "File processing", size=12, color=RED, bold=True)
f.text(440, 14, "Database approach", size=12, color=TEAL, bold=True)
for i, (name, st, fl) in enumerate([("Library file", RED, ROSE), ("Exam file", RED, ROSE), ("Fee file", RED, ROSE)]):
    x = 8 + i * 94
    f.box(x, 30, 86, 30, name, fill=fl, stroke=st, size=10, bold=True)
    f.box(x, 66, 86, 44, "Sita\nKirtipur\n(old address)" if i != 1 else "Sita\nPatan\n(NEW address)", fill=SOFT, stroke=st, size=9.5)
f.text(145, 134, "three copies, only one updated", size=10, color=RED, bold=True)
f.text(145, 150, "admit card goes to the wrong house", size=10, color=SLATE)
f.box(340, 30, 200, 30, "Student table (one copy)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(340, 66, 200, 44, "Sita | Patan", fill=SOFT, stroke=TEAL, size=11, bold=True)
for i, nm in enumerate(["Library app", "Exam app", "Fee app"]):
    x = 330 + i * 74
    f.box(x, 160, 68, 28, nm, fill=BLUE, stroke=NAVY, size=9.5, bold=True)
    f.arrow([(x + 34, 160), (440, 110)], color=TEAL, sw=1.3)
f.text(440, 214, "every program sees the same, current address", size=10, color=TEAL, bold=True)
f.text(290, 240, "one fact, one place: consistency by design", size=10.5, color=NAVY, bold=True)
```

```svgfig label="1.2" caption="Where the DBMS sits. Naive users work through forms and apps, analysts type SQL, programmers embed SQL in programs and the DBA looks after the whole system. All requests pass through the DBMS software, whose query processor understands and optimises each request and whose storage manager reads and writes the disk files. The data dictionary (catalog) stores the metadata, and the database itself holds the data."
f = Fig(580, 270)
users = [("Naive user\n(app, form)", 10), ("Analyst\n(SQL)", 125), ("Programmer\n(SQL in code)", 240), ("DBA\n(admin tools)", 355)]
for nm, x in users:
    f.box(x, 8, 105, 40, nm, fill=SAND, stroke=AMBER, size=10, bold=True)
    f.arrow([(x + 52, 48), (x + 52, 78)], color=SLATE, sw=1.4)
f.box(10, 78, 450, 110, "", fill=BLUE, stroke=NAVY, sw=2)
f.box(25, 108, 200, 36, "Query processor\n(parse, optimise, execute)", fill=SOFT, stroke=NAVY, size=10, bold=True)
f.box(245, 108, 200, 36, "Storage manager\n(files, buffers, indexes, log)", fill=SOFT, stroke=NAVY, size=10, bold=True)
f.arrow([(225, 126), (245, 126)], color=NAVY, sw=1.4, both=True)
f.text(235, 94, "DBMS software", size=11, color=NAVY, bold=True)
f.text(235, 172, "transaction manager | security | recovery", size=9.5, color=SLATE, bold=True)
f.arrow([(130, 188), (130, 216)], color=SLATE, sw=1.5)
f.arrow([(340, 188), (340, 216)], color=SLATE, sw=1.5)
f.box(30, 216, 200, 40, "Data dictionary\n(metadata: names, types, rules)", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(240, 216, 200, 40, "Database\n(Student, Course, Result ...)", fill=MINT, stroke=TEAL, size=10, bold=True)
f.text(520, 130, "one\nsoftware\nlayer,\nmany\nusers", size=10.5, color=NAVY, bold=True)
```

```svgfig label="1.3" caption="From data to wisdom with one Nepali example. Raw data (marks) are processed into information (average and rank), which a decision maker turns into knowledge and action. Metadata, the description of what each column means, travels beside the data and tells the system how to treat it."
f = Fig(580, 150)
steps = [("Data", "87, 64, 91, 58", SOFT, SLATE), ("Information", "Average 75, rank 2", BLUE, NAVY), ("Knowledge", "Weak in Maths II", MINT, TEAL), ("Action", "Extra class for 3rd sem", SAND, AMBER)]
for i, (a, b, fl, st) in enumerate(steps):
    x = 8 + i * 144
    f.box(x, 20, 124, 62, "", fill=fl, stroke=st, sw=1.8)
    f.text(x + 62, 40, a, size=12, color=st, bold=True)
    f.text(x + 62, 64, b, size=9.5, color=SLATE)
    if i < 3:
        f.arrow([(x + 124, 51), (x + 144, 51)], color=SLATE, sw=1.6)
f.box(8, 104, 564, 32, "Metadata: marks(subject CHAR(8), score INT CHECK 0..100) tells the DBMS what the numbers mean", fill=ROSE, stroke=RED, size=9.5, bold=True)
```

```photogrid label="1.4" cols="2" ratio="1.27" caption="A database is not only about speed; it also removes the waste and the inconsistency of duplicate files. (a) Racks of servers in a data centre, where large public databases are kept. (b) Take a student-style record with an integer roll number, a 30-character name, a 20-character district, a date and a float, which the cell measured as 62 bytes. Stored once for each of the 29,164,578 people of the 2021 census, it needs 1.68 GiB. If three departments keep their own files the cost is 5.05 GiB, so 3.37 GiB is wasted, and a change of address must be repeated three times or the copies disagree."
@ photo id="cs12/datacenter" cap="Servers in a data centre hold the national databases"
fit 1.27
focus 0.5 0.5
@ svg cap="Size of one student table and the cost of copies"
import struct
rec = struct.calcsize("<i30s20sif")
pop = 29164578
one = rec * pop / 2 ** 30
three = 3 * one
saved = three - one
assert rec == 62
f = Fig(300, 236)
f.text(150, 14, "Storing %s people x %d bytes per record" % ("{:,}".format(pop), rec), size=9.5, color=NAVY, bold=True)
f.text(10, 40, "One shared database", size=10, anchor="start", bold=True, color=TEAL)
f.box(10, 48, 280 * one / three, 26, "%.2f GiB" % one, fill=TEAL, stroke=TEAL, color="#ffffff", size=10.5, bold=True, r=3)
f.text(10, 100, "Three department files (copies)", size=10, anchor="start", bold=True, color=RED)
f.box(10, 108, 280, 26, "%.2f GiB" % three, fill=RED, stroke=RED, color="#ffffff", size=10.5, bold=True, r=3)
f.text(150, 160, "record = INT 4 + CHAR 30 + CHAR 20 + DATE 4 + FLOAT 4", size=9, color=SLATE)
f.text(150, 178, "= %d bytes (struct.calcsize)" % rec, size=10, color=NAVY, bold=True)
f.text(150, 198, "files waste %.2f GiB on duplicates" % saved, size=10.5, color=RED, bold=True)
f.text(150, 215, "and one address change needs 3 edits, not 1", size=10.5, color=NAVY, bold=True)
facts = dict(rec=rec, one="%.2f" % one, three="%.2f" % three, saved="%.2f" % saved)
```

### 1.6.1 Eight applications of a DBMS

1. **Banking and digital payments.** A bank stores customers, accounts and every transaction in a DBMS, so a balance is always exact. When you send money with ConnectIPS or Fonepay, the database subtracts from one account and adds to another in a single all-or-nothing transaction. Without a DBMS, a power cut in the middle could lose or duplicate your money.
2. **Airlines, buses and railways.** Reservation systems keep seat tables that hundreds of counters and websites update at the same time. The DBMS locks a seat while one buyer is paying, so two people never receive the same seat. Nepali airlines, long-distance bus counters and online ticket sites all depend on this behaviour.
3. **Education.** A university keeps students, courses, fees, attendance and results in one database. Tribhuvan University and NEB result services, college admission portals and the EMIS records of schools answer thousands of result look-ups in a few seconds. One record per student prevents the old problem of different marks in different offices.
4. **Government and public services.** Citizenship, the national identity card, driving licences, vehicle registration and tax records are database applications. The Nagarik App shows a citizen's documents by reading records that departments keep in databases. Central storage allows one office to verify data held by another without paper letters.
5. **Telecom and utilities.** Nepal Telecom, Ncell and the electricity authority keep call records, SIM registrations, meter readings and bills for millions of customers. A DBMS summarises usage each month and produces the correct bill for each person. It also helps to find faults and detect unusual use.
6. **Healthcare.** Hospitals store patient history, test reports, prescriptions and bed allocation. A doctor in the emergency room can see allergies and past treatment within seconds, which can save a life. Access control keeps a patient's record private from people who have no need to see it.
7. **Retail and e-commerce.** Online shops such as Daraz keep products, stock, orders, payments and delivery status in databases. When two customers try to buy the last item, the DBMS decides which order succeeds. Sales reports and recommendations are built by querying the same data.
8. **Social media, media and apps.** Profiles, posts, friendships, comments and notifications are rows in very large databases. Study apps such as the NEBians app store notes, progress and bookmarks for each learner. The DBMS makes sure that a deleted post disappears everywhere and that each user sees only what they are allowed to see.

## Formula and fact sheet

- Data → processed → information. Metadata lives in the data dictionary.
- DBMS goals: reduce redundancy, share data, enforce integrity and security, support transactions, provide data independence.
- Users: DBA, designer, programmer, sophisticated user, naive user.

## Chapter summary

- A DBMS manages a database for many users with consistency, security and recovery.
- It replaces the redundancy, isolation and integrity problems of file processing.
- Costs are money, complexity and overhead; benefits grow with data size and number of users.

## Practice

1. Differentiate data, information and metadata.
2. List five drawbacks of the file-processing system and the DBMS feature that fixes each.
3. State four merits and three demerits of a DBMS.
4. Name five applications of DBMS.
5. Explain the roles of a DBA and of an application programmer.
6. When would a DBMS not be worth using?

::: note Answers and worked solutions
**1.** Data: raw facts. Information: processed, meaningful data. Metadata: data about the structure of the data (names, types, constraints), stored in the catalog.
**2.** Redundancy → controlled redundancy; difficult access → SQL; integrity in code → declared constraints; concurrent anomalies → concurrency control; poor security → authorisation.
**3.** Merits: less redundancy, integrity, security, backup/recovery. Demerits: cost, complexity, overhead.
**4.** Banking, railway reservation, university results, e-commerce, hospital records.
**5.** The DBA manages the physical database, security, backup and performance. The application programmer writes the programs that read and update the database through SQL.
**6.** A small, single-user, simple-structure task with no concurrency or security needs.
:::

## Model answers (5 and 10 marks)

**Q1 (5 marks). Explain the disadvantages of the file-processing system and show how a DBMS removes them.**

*Introduction.* In file processing every application keeps its own files in its own format, as in the left half of Figure 1.1. This works for a very small job but becomes difficult as data and users grow.

1. **Redundancy and inconsistency.** The same address is stored in the library, exam and fee files. If only one copy is changed, the files disagree. A DBMS stores the fact once and lets every program share it.
2. **Difficult access.** A new question, such as "list all students with more than 80 marks in two subjects", needs a new program. A DBMS answers it with one SQL query.
3. **Data isolation.** Files have different formats, so combining them is hard. A DBMS uses one data model and one catalog.
4. **Integrity problems.** A rule like "marks must be 0 to 100" is hidden in program code and can be forgotten. A DBMS declares the rule once as a constraint.
5. **Atomicity and concurrency problems.** A crash in the middle of a fund transfer, or two clerks updating one balance together, leaves wrong data. A DBMS provides transactions, logging and locking.
6. **Security problems.** File systems give all-or-nothing access, while a DBMS can allow one user to see only one table or column.

*Example.* A bank's file system could show a balance reduced but not credited after a power cut; a DBMS would undo the half-finished transfer.

*Conclusion.* The DBMS replaces scattered files with one controlled, shared, secure and recoverable store, at the cost of money and complexity.

**Q2 (5 marks). Define DBMS. Explain its merits and demerits.**

*Introduction.* A database is an organised collection of related data and a Database Management System (DBMS) is the software, such as MySQL, Oracle or PostgreSQL, that creates, stores, protects and queries it (Figure 1.2).

*Merits.*
1. **Controlled redundancy:** each fact is stored once, which saves space and avoids inconsistency.
2. **Data sharing:** many users and programs use the same data at the same time.
3. **Integrity:** constraints such as primary key and CHECK are enforced centrally.
4. **Security:** the DBA grants each user only the privileges that user needs.
5. **Backup and recovery:** the log lets the system restore a consistent state after a failure.
6. **Data independence:** the physical storage can change without rewriting application programs.
7. **Faster development:** programmers use SQL instead of writing file-handling code.

*Demerits.*
1. **Cost:** software licences, powerful hardware and trained staff are expensive.
2. **Complexity:** design, tuning and administration need skill.
3. **Overhead:** locking, logging and checking consume time and storage.
4. **Single point of failure:** if the central database stops, every application stops unless it is replicated.
5. **Conversion cost:** moving old file data into a database takes effort.

*Conclusion.* The merits grow with the size of data and the number of users, so a college or bank should use a DBMS, while a small personal list can stay in a spreadsheet.

**Q3 (10 marks). Describe the database system environment. Explain the objectives of a DBMS, the people who work with it and its applications.**

*Introduction.* A database system is the combination of the database, the DBMS software, the hardware, the application programs and the people who use them. Its purpose is to store the data of an organisation once and let many users share it safely. Figure 1.2 shows how the parts fit together.

*Architecture.* Users reach the data only through the DBMS. The query processor parses each SQL statement, chooses an efficient plan and executes it. The storage manager reads and writes disk files, manages buffers and indexes and writes the log. The data dictionary keeps metadata, and the database holds the data itself.

*Objectives of a DBMS.*
1. **Reduce redundancy** so that one fact is stored in one place (Figure 1.1).
2. **Give easy access** to data through a query language.
3. **Provide one data model** so that data from many sources can be combined.
4. **Enforce integrity** through declared constraints.
5. **Guarantee atomicity** so that a transaction is done completely or not at all.
6. **Control concurrency** so that simultaneous users do not corrupt each other's work.
7. **Provide security** through user accounts and privileges.
8. **Give data independence** so that programs survive changes in storage.

*People.* The database administrator (DBA) designs the physical database, grants access, tunes performance and manages backup. The database designer chooses the schema. Application programmers write programs that use SQL. Sophisticated users such as analysts type queries directly, and naive users, such as bank clerks or online shoppers, use forms and apps.

*Applications.* Banking and ConnectIPS payments, ticket reservation, university results, telecom billing, hospital records, government services such as the Nagarik App, retail sales and social media all run on a DBMS (Section 1.6.1).

| Point | File system | DBMS |
|---|---|---|
| Redundancy | high | controlled |
| Query | new program for each question | SQL |
| Integrity | in program code | declared constraints |
| Concurrency | anomalies | locking and transactions |
| Recovery | manual | log-based, automatic |
| Cost | low | higher |

*Conclusion.* A DBMS is the heart of any organisation that must keep large, shared, accurate and secure data, and the objectives above explain why it replaced file processing.
