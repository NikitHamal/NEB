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
