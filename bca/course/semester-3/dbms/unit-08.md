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

## 8.11 Seeing the ideas: plans, costs and defences

A database has two big jobs after it is designed: to answer queries cheaply and to keep its data safe. The figures below show how the optimiser chooses a plan, how much that choice is worth, and how the layers of protection and the privileges of the DBA work. The security statements were tested on a real PostgreSQL server with two test roles, clerk and teacher.

```photogrid label="8.1" cols="3" ratio="1.0" caption="Safeguarding data in the physical world. (a) A robotic tape library: copies of the database are written to tape and kept away from the server, so that a fire, a flood or a ransomware attack does not destroy every copy; backups are part of the DBA's duty. (b) A hardware security module (HSM), a tamper-resistant device that stores encryption keys apart from the data they protect. (c) A padlock, the oldest symbol of access control: only the holder of the right key may open it, which is the idea of authentication and authorisation in a DBMS."
@ photo id="bca202/tapelib" cap="Tape library for backups"
fit 1.0
focus 0.5 0.5
call 0.5 0.1 0.55 0.5 "offline copies"
@ photo id="bca451/hsm" cap="Hardware security module"
fit 1.0
focus 0.5 0.5
@ photo id="bca306/padlock" cap="Padlock: access control"
fit 1.0
focus 0.5 0.5
```

```svgfig label="8.1" caption="The three stages of query processing. The parser checks the syntax and the names against the catalog and translates the SQL text into a relational-algebra expression. The optimiser generates equivalent expressions and algorithm choices, estimates the cost of each with statistics from the catalog (table sizes, index heights, value distributions) and picks the cheapest evaluation plan. The execution engine runs the chosen plan against the stored data and returns the rows. EXPLAIN shows the plan that was chosen."
f = Fig(580, 190)
f.box(6, 60, 80, 50, "SQL\nquery", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(110, 40, 100, 90, "1 Parser and\ntranslator\n(syntax, names,\nalgebra)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(240, 40, 110, 90, "2 Optimiser\n(many plans,\nestimate cost,\nchoose cheapest)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(380, 40, 100, 90, "3 Execution\nengine\n(run the plan)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.box(505, 60, 70, 50, "Result\nrows", fill=SAND, stroke=AMBER, size=11, bold=True)
for a, b in [(86, 110), (210, 240), (350, 380), (480, 505)]:
    f.arrow([(a, 85), (b, 85)], color=SLATE, sw=1.6)
f.box(240, 150, 110, 30, "Catalog statistics", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.arrow([(295, 150), (295, 130)], color=SLATE, sw=1.4)
f.box(380, 150, 100, 30, "Data and indexes", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.arrow([(430, 150), (430, 130)], color=SLATE, sw=1.4, both=True)
f.text(110, 20, "relational algebra", size=9, color=NAVY, bold=True, anchor="start")
f.text(240, 20, "evaluation plan", size=9, color=TEAL, bold=True, anchor="start")
```

```svgfig label="8.2" caption="The cost of joining Student (400 blocks, 10,000 records) with Enrollment (1,000 blocks, 50,000 records) on sid with 52 buffer blocks. The bars use a logarithmic scale, because the costs run from 1,400 to 10,000,400 block transfers. Plain tuple-at-a-time nested loop is the worst at 10,000,400. Using the memory buffers well (block nested loop with 50 buffers) gives 8,400, an index on the inner table gives 40,400, a hash join gives about 4,200 and a merge join of already sorted inputs gives 1,400. The best plan is about 7,000 times cheaper than the worst, which is why query optimisation matters."
f = Fig(580, 230)
import math
data = [("Nested loop (tuple at a time)", 10000400, RED, ROSE), ("Block nested loop (1 buffer)", 400400, RED, ROSE), ("Indexed nested loop", 40400, AMBER, SAND), ("Block nested loop (50 buffers)", 8400, AMBER, SAND), ("Hash join", 4200, TEAL, MINT), ("Merge join (sorted inputs)", 1400, TEAL, MINT)]
f.text(290, 12, "Block transfers (log scale)", size=10.5, color=NAVY, bold=True)
for i, (nm, v, st, fl) in enumerate(data):
    y = 26 + i * 30
    w = (math.log10(v) - 2.5) * 105
    f.text(8, y + 13, nm, size=9.5, color=SLATE, bold=True, anchor="start", vmid=True)
    f.box(200, y, w, 22, "", fill=fl, stroke=st, sw=1.4)
    f.text(200 + w + 6, y + 11, f"{v:,}", size=10, color=st, bold=True, anchor="start", vmid=True)
f.text(290, 216, "worst / best = 10,000,400 / 1,400 = about 7,100 times", size=10.5, color=RED, bold=True)
```

```svgfig label="8.3" caption="Defence in depth. Security is built in layers, so that if one layer fails the next still protects the data. From the outside in: physical security of the server room, the network (firewall, TLS), the operating system (patches, restricted accounts), the database itself (authentication, authorisation, audit, encryption), the application (input checks and parameterised queries against SQL injection) and finally people (training and separation of duties). The data sit at the centre."
f = Fig(580, 270)
layers = [("Physical: locked room, UPS, offsite backup", 560, 255, SOFT, SLATE), ("Network: firewall, TLS, VPN", 480, 217, BLUE, NAVY), ("Operating system: patches, accounts", 400, 179, MINT, TEAL), ("Database: login, GRANT, audit, encryption", 320, 141, SAND, AMBER), ("Application: input checks, parameters", 240, 103, ROSE, RED), ("People: training, duties", 160, 65, BLUE, NAVY)]
for i, (t, w, h, fl, st) in enumerate(layers):
    f.box(290 - w / 2, 8 + i * 19 - 0, w, 254 - i * 38, "", fill=fl, stroke=st, sw=1.5)
for i, (t, w, h, fl, st) in enumerate(layers):
    f.text(290, 20 + i * 19, t, size=9.5, color=st, bold=True)
f.box(240, 150, 100, 44, "DATA", fill=NAVY, stroke=NAVY, color="#ffffff", size=14, bold=True)
```

```svgfig label="8.4" caption="Two models of access control. In discretionary access control (left) the owner decides: the DBA grants SELECT to the clerk, and WITH GRANT OPTION lets the clerk pass the right on. The teacher was granted SELECT and UPDATE on the column marks only; on the real server the clerk (who could read only sid and cid) got permission denied for table enrollment when trying SELECT * or UPDATE, and the teacher's DELETE and UPDATE of cid were refused. REVOKE UPDATE (marks) then removed the teacher's last right. In mandatory access control (right) the system compares the label of the user with the label of the data: a user may read at or below their clearance and write only at or above it."
f = Fig(580, 270)
f.text(145, 12, "Discretionary (GRANT / REVOKE)", size=10.5, color=NAVY, bold=True)
f.box(80, 24, 130, 30, "Owner / DBA", fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True)
f.box(10, 100, 120, 44, "Clerk\nSELECT (sid, cid)", fill=MINT, stroke=TEAL, size=9, bold=True)
f.box(160, 100, 120, 44, "Teacher\nSELECT; UPDATE (marks)", fill=MINT, stroke=TEAL, size=9, bold=True)
f.arrow([(130, 54), (70, 100)], color=TEAL, sw=1.6, label="GRANT", lpos=(80, 70), lsize=8.5)
f.arrow([(160, 54), (220, 100)], color=TEAL, sw=1.6, label="GRANT", lpos=(210, 70), lsize=8.5)
f.arrow([(220, 144), (220, 168)], color=RED, sw=1.6, dash=True)
f.box(160, 168, 120, 30, "REVOKE UPDATE (marks)", fill=ROSE, stroke=RED, size=8.5, bold=True)
f.box(10, 210, 270, 48, "Real error for a missing right:\npermission denied for table enrollment", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
f.text(435, 12, "Mandatory (labels)", size=10.5, color=RED, bold=True)
lv = [("Top Secret", ROSE, RED), ("Secret", SAND, AMBER), ("Confidential", BLUE, NAVY), ("Unclassified", MINT, TEAL)]
for i, (n, fl, st) in enumerate(lv):
    f.box(340, 28 + i * 40, 110, 34, n, fill=fl, stroke=st, size=10.5, bold=True)
f.arrow([(470, 150), (470, 40)], color=TEAL, sw=1.8)
f.text(478, 100, "read\ndown", size=9, color=TEAL, bold=True, anchor="start")
f.arrow([(530, 40), (530, 150)], color=RED, sw=1.8)
f.text(538, 120, "write\nup", size=9, color=RED, bold=True, anchor="start")
f.box(330, 200, 240, 58, "A Secret user reads Secret and below,\nbut cannot copy data down to a\nlower label: stops Trojan-horse leaks", fill=SOFT, stroke=SLATE, size=9, bold=True)
```

```svgfig label="8.5" caption="Three cryptographic tools in a database. Symmetric encryption (AES) uses one secret key to encrypt and decrypt and is fast enough for whole tables and backups. Asymmetric encryption (RSA, ECC) uses a public and a private key and is used to exchange keys and sign messages. A hash such as SHA-256 is one-way: it cannot be decrypted and is used to store passwords. SHA-256 of the text password begins 5e884898da280471, while changing only the capital letter (Password) gives e7cf3ef4f17c3999, and 140 of the 256 output bits change."
f = Fig(580, 200)
f.box(6, 14, 180, 100, "Symmetric (AES)\none key both ways\nfast: bulk data,\ncolumns, backups", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(200, 14, 180, 100, "Asymmetric (RSA, ECC)\npublic key encrypts,\nprivate key decrypts\nslow: keys, signatures", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(394, 14, 180, 100, "Hash (SHA-256, bcrypt)\none-way, no key\npassword storage,\nintegrity checks", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(6, 130, 568, 62, "password -> 5e884898da280471...      Password -> e7cf3ef4f17c3999...\n140 of 256 bits changed for a one-letter change (avalanche effect)\nStore the key in a key vault or HSM, never beside the encrypted data", fill=SOFT, stroke=SLATE, size=10, bold=True)
```

### 8.11.1 Eight responsibilities of a database administrator

1. **Designing and changing the schema.** The DBA creates tables, keys and constraints with the designers and applies changes safely when requirements grow. A new column in a student table must be added without breaking the programs that already use it. Careful change control prevents mistakes in a live system.
2. **Choosing storage and indexes.** The DBA decides how data are stored and which columns are indexed. Using the query plans of Figures 8.1 and 8.2, a missing index can be found and a slow report made fast. Good choices save both time and hardware cost.
3. **Managing users and privileges.** Each person gets an account and only the rights needed for the job, using roles and GRANT and REVOKE (Figure 8.4). A clerk may read names but not change marks. When a person leaves a college, the DBA removes the account at once.
4. **Backup and recovery.** The DBA takes regular full and incremental backups, stores copies offsite (Plate 8.1) and tests restoring them. A backup that has never been restored is only a hope. Good recovery plans let a Nepali bank resume work within hours after a disaster.
5. **Monitoring and performance tuning.** The DBA watches response time, disk space, locks and slow queries. Problems are fixed before users complain, for example by adding memory or rewriting a query. In an examination-result week the traffic can grow several times, and the DBA prepares for it.
6. **Security and auditing.** The DBA turns on audit trails to record logins, failed attempts and changes to sensitive tables. These records help to find who changed a mark and when. Regular reviews catch weak passwords and unusual activity.
7. **Encryption and key management.** Sensitive data such as passwords, citizenship numbers and bank details are encrypted at rest and in transit, and keys are kept in a vault or HSM. Passwords are stored only as salted hashes (Figure 8.5). A stolen disk then reveals nothing useful.
8. **Availability and capacity planning.** The DBA plans replication, failover and growth, so that the database stays available when a server fails and has room for next year's data. Software patches are applied at planned times with warning to users. This is how services such as online results and payments stay up.

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

## Model answers (5 and 10 marks)

**Q1 (5 marks). Explain the steps of query processing.**

*Introduction.* Query processing is the set of activities from receiving a SQL statement to returning its result. Because SQL states only what is wanted, the DBMS must decide how to get it (Figure 8.1).

1. **Parsing and translation.** The parser checks the syntax, checks that the tables and columns exist in the catalog, and translates the query into a relational-algebra expression such as π_name(σ_marks>80(Student ⋈ Enrollment)).
2. **Optimisation.** The same query has many equivalent expressions (for example selecting before joining) and many algorithms for each operator. The optimiser estimates the cost of each plan from catalog statistics and chooses the cheapest evaluation plan.
3. **Evaluation.** The execution engine runs the chosen plan, reading blocks through the buffer, and returns the rows to the user.
4. **Cost measure.** Cost is mostly the number of block transfers from disk plus the number of seeks. A full scan costs b_r blocks, while a B+ tree equality search costs the height h plus one.
5. **Example of the gain.** For the join of Student (400 blocks) with Enrollment (1,000 blocks), plain nested loop costs 10,000,400 block transfers while a merge join of sorted inputs costs 1,400.

*Conclusion.* Parsing, optimisation and evaluation turn a declarative query into an efficient plan, and the optimiser's choice can change the cost by thousands of times.

**Q2 (5 marks). Differentiate between discretionary and mandatory access control.**

*Introduction.* Access control decides which authenticated user may do which operation on which object. The two classic models are discretionary and mandatory (Figure 8.4).

1. **Discretionary access control (DAC).** The owner of an object grants and revokes privileges with `GRANT` and `REVOKE`. Privileges include SELECT, INSERT, UPDATE (also by column), DELETE and REFERENCES. For example `GRANT SELECT, UPDATE (marks) ON enrollment TO teacher;`.
2. **Grant option.** `WITH GRANT OPTION` lets the receiver pass the privilege on, and a REVOKE removes it from the whole chain.
3. **Weakness of DAC.** A user who may read data can copy it into his own table and share it, which is the Trojan-horse problem.
4. **Mandatory access control (MAC).** The system gives each object a classification and each user a clearance, such as Top Secret, Secret, Confidential and Unclassified. A user reads only at or below the clearance and writes only at or above it, so information cannot flow downward.
5. **Use.** DAC suits ordinary business systems and colleges; MAC suits military and intelligence systems where strict rules are required.

| Point | DAC | MAC |
|---|---|---|
| Who decides | owner | system policy |
| Flexibility | high | low |
| Security | weaker | stronger |

*Test.* On a real server a user without the right received "permission denied for table enrollment".

*Conclusion.* DAC is flexible and owner controlled, while MAC is rigid and system controlled and therefore stronger against leaks.

**Q3 (10 marks). Describe the role of a database administrator. Explain the security issues of a database and the measures that protect it, including encryption.**

*Introduction.* The database administrator (DBA) is the person or team responsible for the whole database system: its design, performance, availability and security. Security means protecting data from loss, theft and unauthorised change, and it matters because a college, bank or hospital holds data that people trust it to keep safe.

*Role of the DBA.* The DBA defines and changes the schema, chooses storage structures and indexes, creates user accounts and roles, grants privileges, takes backups and plans recovery, monitors performance and tunes queries, switches on auditing, manages encryption keys and plans capacity and availability (Section 8.11.1).

*Security threats.* Weak or stolen passwords, insiders who misuse rights, SQL injection from careless applications, malware and ransomware, physical theft of disks or backups, network eavesdropping, and mistakes by authorised users.

*Security measures (Figure 8.3).*
1. **Physical:** locked server room, power backup and offsite backup copies.
2. **Network:** firewall, VPN and TLS-encrypted connections.
3. **Operating system:** patches and restricted administrator accounts.
4. **Database:** authentication, authorisation with roles and GRANT and REVOKE, and an audit trail of logins and changes.
5. **Application:** input validation and parameterised queries to stop SQL injection, and service accounts with least privilege.
6. **Human:** training and separation of duties, so that no single person can both change and approve.

*Encryption.* Encryption turns plaintext into ciphertext with a key, and decryption reverses it. Symmetric encryption such as AES uses one key and is fast, so it protects tables, disks and backups. Asymmetric encryption such as RSA uses a public and a private key and is used for key exchange and digital signatures. Hashing such as SHA-256 or bcrypt is one-way and is used to store passwords: a one-letter change in the password changed 140 of 256 output bits. Data are protected at rest and in transit, and the keys are kept in a vault or hardware security module, separate from the data.

| Layer | Example measure |
|---|---|
| Physical | locked room, offsite tape |
| Network | TLS, firewall |
| Database | GRANT, audit trail, encryption |
| Application | parameterised queries |

*Conclusion.* No single measure is enough, so the DBA combines several layers of defence, controls privileges strictly, encrypts sensitive data and keeps tested backups, which together protect the confidentiality, integrity and availability of the data.
