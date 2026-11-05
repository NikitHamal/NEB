---
subject: Database Management System
grade: BCA Semester 3
unit: 8
title: Query Processing and Security
hours: 5
area: BCA 202 · Database Management System · Unit 8
---

This unit has two halves: how the DBMS **executes** a query efficiently (processing, cost, optimisation), and how it **protects** the data (the DBA's work, access control and encryption).

::: key What this unit gives you
- The steps of query processing and the cost measure (block transfers).
- Algorithms for selection, sorting and join, with worked cost numbers.
- Expression evaluation and heuristic optimisation.
- DBA roles; security types, user accounts, audits, discretionary and mandatory access control, encryption, SQL injection.
:::

## 8.1 Overview of query processing

A query goes through three stages:

1. **Parsing and translation:** check syntax and names against the catalog; translate the SQL to a relational-algebra expression.
2. **Optimisation:** among many equivalent expressions and algorithms, choose the **evaluation plan** with the lowest estimated cost.
3. **Evaluation:** the execution engine runs the plan and returns rows.

`EXPLAIN` (PostgreSQL, MySQL) or `EXPLAIN PLAN` (Oracle) shows the chosen plan.

## 8.2 Measuring query cost

Disk is far slower than memory, so cost is estimated mostly as **block transfers** (plus a smaller number of seeks). Notation: **n_r** records and **b_r** blocks of relation r; **M** memory buffer blocks; **h** height of a B+ tree index. Cost depends on the algorithm, the buffer size and the data distribution; the optimiser uses **statistics** from the catalog (row counts, distinct values, histograms).

## 8.3 Selection operation

For σ_A=v(r), with Enrollment: n = 50,000 records in b = 1,000 blocks, B+ tree height h = 3:

| Algorithm | Cost (block transfers) | Applies |
|---|---|---|
| **Linear scan** | b = 1,000 (equality on a key: average b/2 = 500) | always |
| **Binary search** | ⌈log₂ b⌉ = 10 (+ blocks with further matches) | file sorted on A |
| **Primary index, key equality** | h + 1 = 4 | index on key |
| **Primary index, range** | h + (blocks holding matching records) | index on sort field |
| **Secondary index, equality** | h + 1 for a key; up to h + (number of matches) otherwise | secondary index |

Conjunctions (`A = 1 AND B = 2`) use the most selective index, or the intersection of record-id lists; disjunctions need indexes on all parts or a scan.

## 8.4 Sorting

Sorting supports `ORDER BY`, duplicate elimination, merge join and grouping. If the data fits in memory, quick sort. Otherwise **external merge sort**: read M blocks at a time, sort them, write sorted **runs**; then merge up to M − 1 runs at a time. Number of runs = ⌈b/M⌉; merge passes = ⌈log_{M−1}(b/M)⌉; total transfers ≈ 2b × (1 + passes) counting the final write.

::: example Worked example: sorting Student (b = 400) and Enrollment (b = 1,000) with M = 52
Student: runs = ⌈400/52⌉ = 8; one merge pass (8 ≤ 51) → 2 × 400 × 2 = **1,600** transfers. Enrollment: runs = ⌈1000/52⌉ = 20; one pass → 2 × 1,000 × 2 = **4,000** transfers.
:::

## 8.5 Join operation

Join Student (n_r = 10,000 records, b_r = 400 blocks) with Enrollment (n_s = 50,000, b_s = 1,000) on `sid`, M = 52 buffer blocks. The outer relation is r = Student.

| Algorithm | Idea | Cost | Result |
|---|---|---|---|
| **Nested-loop** (tuple at a time) | for each r-tuple scan all of s | n_r·b_s + b_r | 10,000 × 1,000 + 400 = **10,000,400** |
| **Block nested-loop** (1 buffer for r) | for each r-block scan s | b_r·b_s + b_r | 400 × 1,000 + 400 = **400,400** |
| **Block nested-loop**, M − 2 buffers for r | for each chunk of M − 2 r-blocks scan s | ⌈b_r/(M−2)⌉·b_s + b_r | 8 × 1,000 + 400 = **8,400** |
| **Indexed nested-loop** | index on s.sid, c ≈ 4 transfers per lookup | b_r + n_r·c | 400 + 10,000 × 4 = **40,400** |
| **Merge join** (both sorted on sid) | merge the two sorted files | b_r + b_s | **1,400** (+ 1,600 + 4,000 if sorting is needed = 7,000) |
| **Hash join** | partition both by hash, join matching partitions | ≈ 3(b_r + b_s) | **4,200** (needs M > √b_r) |

The same logical join differs by a factor of **7,000** between the best and worst algorithm: this is why the optimiser matters. Merge and hash joins handle equi-joins; nested loop handles any condition; always put the **smaller relation as the outer** one.

## 8.6 Evaluation of expressions and optimisation

An expression tree can be evaluated by **materialisation** (compute each operator completely, store the temporary result on disk, then pass to the next) or by **pipelining** (pass each tuple to the parent as it is produced, with no temporary file). Pipelining is cheaper but not possible for blocking operators such as a full sort.

**Query optimisation.** Equivalent algebra expressions give the same result at different cost. Useful **equivalence rules**: a conjunctive selection can be split, σ_{θ1∧θ2}(E) = σ_θ1(σ_θ2(E)); selections commute; **selection pushes through a join** when it involves only one side's attributes; only the last of a cascade of projections is needed; joins are commutative and associative; σ over a union distributes.

**Heuristic optimisation rules:** (1) perform **selections as early as possible**; (2) perform **projections early**, dropping unneeded columns; (3) combine a selection with a Cartesian product into a join; (4) order joins so the smallest intermediate results come first; (5) use available indexes. **Cost-based optimisers** (all modern DBMSs) enumerate plans, estimate each with statistics, and keep the cheapest.

::: example Worked example: pushing a selection below a join
Query: names of students with marks above 80. Naïve plan: join Student (10,000) with Enrollment (50,000) giving 50,000 intermediate rows, then filter. Better: filter Enrollment first. If 5% of rows have marks > 80, that is 2,500 rows, so the join handles 2,500 instead of 50,000 rows: **20 times** less intermediate data. A later projection on `name` and `sid` keeps rows narrow.
:::

## 8.7 The database administrator and security issues

The **DBA** is responsible for: schema definition and changes; storage structure and index selection; **user accounts and authorisation**; **backup and recovery**; monitoring and **performance tuning**; **security and auditing**; ensuring integrity and availability; capacity planning and upgrades.

**Security** protects data from loss, theft and unauthorised change. Threats: unauthorised access (stolen or weak passwords), insiders, SQL injection, malware, physical theft, network eavesdropping, accidental destruction. Levels of protection:

| Level | Measures |
|---|---|
| **Physical** | locked server room, power backup, offsite backups |
| **Network** | firewalls, TLS encryption of connections, VPN |
| **Operating system** | patching, restricted accounts |
| **Database** | authentication, authorisation, auditing, encryption |
| **Application** | input validation, parameterised queries, least-privilege service accounts |
| **Human** | training, separation of duties |

## 8.8 Access protection, user accounts and audits

**Authentication** proves who you are (password, certificate, token, multi-factor); **authorisation** decides what you may do. The DBA creates **user accounts**, usually grouped into **roles**, each with the minimum rights needed (**least privilege**). Passwords are stored only as salted **hashes**.

```text
CREATE USER clerk IDENTIFIED BY "s3cret!";      -- Oracle
CREATE ROLE reporting;
GRANT SELECT ON student_results TO reporting;
GRANT reporting TO clerk;
```

A **database audit** records who did what and when (logins, failed attempts, DDL, access to sensitive tables) in an **audit trail** that is protected from alteration; it supports accountability, detection of intrusion and legal compliance. It can be built with triggers (Unit 7) or native auditing (Oracle `AUDIT`, PostgreSQL `pgaudit`).

## 8.9 Discretionary and mandatory access control

**Discretionary access control (DAC):** the *owner* of an object grants or revokes privileges to other users with `GRANT` and `REVOKE`. Privileges: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REFERENCES`, `EXECUTE`, and system privileges. `WITH GRANT OPTION` lets the recipient pass the privilege on; `REVOKE` can cascade. Views implement row- or column-level restriction.

```text
GRANT SELECT, UPDATE (marks) ON enrollment TO teacher;     -- column-level update
GRANT SELECT ON student TO clerk WITH GRANT OPTION;
REVOKE UPDATE ON enrollment FROM teacher;
```

DAC is flexible but vulnerable: a user with read access can copy data and pass it on (**Trojan horse** problem).

**Mandatory access control (MAC):** the *system* enforces rules based on **security classification** of objects and **clearance** of subjects, levels such as Top Secret > Secret > Confidential > Unclassified. The **Bell–LaPadula** model: **no read up** (a subject may read only objects at or below its level) and **no write down** (it may write only at or above its level, so secrets cannot leak downward). Users cannot override it. Used in military and intelligence systems; **role-based access control (RBAC)** is the common compromise in businesses.

## 8.10 Data encryption and decryption

**Encryption** converts plaintext to unreadable **ciphertext** with a key; **decryption** reverses it.

| Kind | Keys | Examples | Use |
|---|---|---|---|
| **Symmetric** | same secret key both ways; fast | AES-256 | bulk data, disk and column encryption |
| **Asymmetric (public key)** | public key encrypts, private key decrypts; slow | RSA, ECC | key exchange, digital signatures, TLS handshake |
| **Hashing** (one-way) | none; cannot be reversed | SHA-256, bcrypt, Argon2 | password storage, integrity checks |

Data should be protected **at rest** (Transparent Data Encryption, encrypted columns, encrypted backups) and **in transit** (TLS). Keys must be stored separately from the data (key vault / HSM). A toy example, the Caesar shift: with key 3, `DBMS` becomes `GEPV`; real systems use AES because a shift is broken in seconds.

**SQL injection.** If an application builds `"SELECT * FROM users WHERE name='" + input + "'"`, the input `' OR '1'='1` makes the condition always true and returns every user; `'; DROP TABLE users; --` runs a second statement. Defence: **parameterised queries / prepared statements** (the value is never parsed as SQL), stored procedures with typed parameters, input validation, and least-privilege accounts.

## Formula and fact sheet

- Query processing: parse → optimise → evaluate. Cost ≈ block transfers.
- Selection: linear b; binary ⌈log₂ b⌉; index h + 1.
- Block nested-loop with M − 2 buffers: ⌈b_r/(M−2)⌉·b_s + b_r. Merge join b_r + b_s. Hash join ≈ 3(b_r + b_s).
- External sort: runs ⌈b/M⌉, passes ⌈log_{M−1}(b/M)⌉.
- Optimise: selections and projections early; smaller relation outer.
- DAC: GRANT/REVOKE by owner. MAC: Bell–LaPadula, no read up, no write down.
- Symmetric (AES) fast; asymmetric (RSA) for key exchange; hash passwords with salt.

## Chapter summary

- The optimiser picks a plan by estimated block transfers; join algorithm choice changes cost by orders of magnitude.
- Heuristics (push selections and projections down) and cost-based search find good plans.
- The DBA secures the database through accounts, roles, least privilege, audit trails and backups.
- DAC lets owners share; MAC enforces classification; encryption protects data at rest and in transit; parameterised queries stop injection.

## Practice

1. Describe the steps of query processing.
2. For a file of 2,000 blocks, estimate the cost of a linear scan, binary search and a B+ tree lookup of height 4.
3. Student has b = 200 blocks and Enrollment b = 800; M = 22. Compute the block-nested-loop join cost with Student as outer.
4. Why is the smaller relation placed as the outer relation?
5. State five heuristic rules of optimisation.
6. List the responsibilities of a DBA.
7. Differentiate DAC and MAC. State the Bell–LaPadula rules.
8. Explain SQL injection and two defences.
9. Differentiate symmetric and asymmetric encryption; why hash passwords?

::: note Answers and worked solutions
**1.** Parsing/translation to relational algebra, optimisation to an evaluation plan, evaluation by the execution engine.
**2.** Linear scan: 2,000 transfers; binary search: ⌈log₂ 2000⌉ = 11; B+ tree: 4 + 1 = 5.
**3.** ⌈200/(22 − 2)⌉ = 10 chunks; 10 × 800 + 200 = **8,200** transfers.
**4.** The cost b_r·b_s/(M−2) + b_r is smaller when the smaller relation drives the outer loop, since the inner relation is rescanned once per chunk of the outer; fewer chunks means fewer rescans.
**5.** Selections early; projections early; combine selection and product into a join; smallest intermediate results first in join order; use indexes.
**6.** Schema design, storage and indexing, accounts and privileges, backup/recovery, performance tuning, security/auditing, integrity and availability.
**7.** DAC: owners grant/revoke rights (flexible, leak-prone). MAC: system-enforced classification and clearance (strict). Bell–LaPadula: no read up, no write down.
**8.** Attacker input is concatenated into SQL and executed as code. Defences: parameterised queries; input validation; least privilege.
**9.** Symmetric: one shared key, fast (AES); asymmetric: public/private key pair, slow, solves key distribution (RSA). Password hashes are one-way, so a stolen table does not reveal passwords, and salting defeats precomputed tables.
:::
