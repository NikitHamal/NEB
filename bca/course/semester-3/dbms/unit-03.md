---
subject: Database Management System
grade: BCA Semester 3
unit: 3
title: Relational Database Model
hours: 4
area: BCA 202 · Database Management System · Unit 3
---

The **relational model** (E. F. Codd, 1970) stores all data in **relations**, informally tables, and manipulates them with a small algebra of operations. It is the foundation of SQL.

::: key What this unit gives you
- Terminology: relation, tuple, attribute, domain, degree, cardinality; schema diagrams.
- Keys: super, candidate, primary, alternate, foreign, composite.
- Integrity rules.
- Relational algebra: select, project, Cartesian product, union, difference, joins.
:::

## 3.1 Structure and terminology

| Formal | Informal | Meaning |
|---|---|---|
| Relation | table | a set of tuples |
| Tuple | row | one record |
| Attribute | column | a named property |
| Domain | data type/allowed values | e.g. marks ∈ [0, 100] |
| Degree | number of columns | |
| Cardinality | number of rows | |

A **relation schema** R(A₁, …, Aₙ) names the attributes; a **database schema** is a set of relation schemas with constraints; a **schema diagram** draws each table with its primary key underlined and arrows from foreign keys to the keys they reference. Properties of a relation: rows are **unordered and distinct**; columns are unordered; each value is **atomic** (single-valued) in a first-normal-form table; **NULL** means unknown or not applicable (it is not zero or blank).

::: example Sample relations used in this unit
**Student**(sid, name, dept_id): (1, Sita, 10), (2, Ram, 10), (3, Hari, 20), (4, Gita, NULL)
**Department**(dept_id, dept_name): (10, BCA), (20, BIT), (30, BBS)
**Enrollment**(sid, cid, marks): (1, C1, 85), (1, C2, 72), (2, C1, 64), (3, C2, 91)
:::

## 3.2 Keys

| Key | Definition |
|---|---|
| **Super key** | any set of attributes that uniquely identifies a tuple (may contain extras): {sid}, {sid, name} |
| **Candidate key** | a *minimal* super key (no attribute can be removed): {sid}; also {email} if unique |
| **Primary key** | the candidate key chosen to identify rows; not NULL; one per table |
| **Alternate key** | candidate keys not chosen as primary |
| **Composite key** | a key of two or more attributes: Enrollment (sid, cid) |
| **Foreign key** | attributes that refer to the primary key of another (or the same) table: Student.dept_id → Department.dept_id |

Every candidate key is a super key; the reverse is false. A table with n attributes where only one attribute is a key has 2^(n−1) super keys.

## 3.3 Integrity constraints

- **Domain constraint:** values come from the attribute's domain (type, range, CHECK).
- **Entity integrity:** no part of a primary key may be NULL.
- **Referential integrity:** a foreign key value must match an existing primary key value, or be NULL. Student (4, Gita, NULL) is legal; inserting dept_id 99 is not. On delete or update of the referenced row the DBMS can **RESTRICT**, **CASCADE**, **SET NULL** or **SET DEFAULT**.
- **Key and unique constraints**, and **semantic** (business) constraints via triggers or assertions.

## 3.4 Relational algebra

A **procedural** query language: operators take relations and return relations, so they compose.

| Operator | Symbol | Meaning |
|---|---|---|
| **Select** | σ_condition(R) | rows satisfying the condition |
| **Project** | π_attrs(R) | chosen columns (duplicates removed) |
| **Union** | R ∪ S | rows in either (union-compatible) |
| **Set difference** | R − S | rows in R not in S |
| **Intersection** | R ∩ S | rows in both = R − (R − S) |
| **Cartesian product** | R × S | every row of R with every row of S; |R|·|S| rows |
| **Rename** | ρ | rename relation or attributes |
| **Natural join** | R ⋈ S | product, keep rows equal on common attributes, drop the duplicate column |
| **Theta/equi join** | R ⋈_θ S | product followed by selection θ |
| **Outer joins** | ⟕ ⟖ ⟗ | like join, but keep unmatched rows of left / right / both, padded with NULL |
| **Division** | R ÷ S | values related to *all* tuples of S ("students who took every course") |

Select, project, union, difference, product and rename are the **fundamental** operators; the rest are derived.

::: example Worked example: queries on the sample data
**σ_dept_id=10(Student)** → (1, Sita, 10), (2, Ram, 10).
**π_name(Student)** → Sita, Ram, Hari, Gita.
**Student ⋈ Department** (on dept_id) → (1, Sita, 10, BCA), (2, Ram, 10, BCA), (3, Hari, 20, BIT). Gita disappears because her dept_id is NULL; BBS disappears because nobody belongs to it.
**Student ⟕ Department** (left outer) adds (4, Gita, NULL, NULL). **Student ⟗ Department** (full outer) also adds (NULL, NULL, 30, BBS).
**π_name(σ_marks>80(Student ⋈ Enrollment))** → Sita (85), Hari (91).
**Students with no enrollment:** π_sid(Student) − π_sid(Enrollment) → {4}.
**Cardinalities:** |Student × Department| = 4 × 3 = 12 rows.
:::

**Expressing a query:** "names of students enrolled in C1" = π_name(Student ⋈ σ_cid='C1'(Enrollment)) → Sita, Ram. Push selections down before joins to make the intermediate result small; this is the idea behind query optimisation (Unit 8).

## 3.5 Seeing the ideas: tables, keys and queries

The relational model is a mathematical idea that became a product. Edgar F. Codd described it in 1970 in the IBM paper "A Relational Model of Data for Large Shared Data Banks" and won the Turing Award for it in 1981. Michael Stonebraker then helped turn the idea into working systems, first Ingres and later Postgres at the University of California, Berkeley; Postgres is the ancestor of the PostgreSQL system that is used all over the world today, and Stonebraker received the Turing Award in 2014.

```photogrid label="3.1" cols="2" ratio="1.1" caption="The relational model in people and in pictures. (a) Michael Stonebraker, creator of the Ingres and Postgres systems; PostgreSQL grew out of his Postgres project and is the database behind many web applications. (b) The anatomy of one relation with the formal terms attached to the informal ones. The Student table has degree 3 (three attributes) and cardinality 4 (four tuples), every column draws its values from a domain, and the primary key sid identifies each tuple."
@ photo id="bca202/stonebraker" cap="Michael Stonebraker"
fit 1.1
focus 0.5 0.55
@ svg cap="Anatomy of the Student relation"
f = Fig(300, 270)
f.text(150, 14, "Student  (relation)", size=11, color=NAVY, bold=True)
hdr = [("sid", 60), ("name", 110), ("dept_id", 80)]
rows = [("1", "Sita", "10"), ("2", "Ram", "10"), ("3", "Hari", "20"), ("4", "Gita", "NULL")]
x0 = 10
for j, (h, w) in enumerate(hdr):
    xx = x0 + sum(a[1] for a in hdr[:j])
    f.box(xx, 30, w, 26, h, fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=0)
    for i, row in enumerate(rows):
        f.box(xx, 56 + i * 26, w, 26, row[j], fill=SOFT if i % 2 else BLUE, stroke=NAVY, size=10, r=0, bold=(j == 0))
f.arrow([(40, 190), (40, 58)], color=TEAL, sw=1.3, label=None)
f.text(10, 200, "attribute = column", size=9.5, color=TEAL, bold=True, anchor="start")
f.text(10, 214, "(sid is the primary key)", size=9.5, color=TEAL, anchor="start")
f.arrow([(270, 190), (230, 82)], color=AMBER, sw=1.3)
f.text(290, 200, "tuple = row", size=9.5, color=AMBER, bold=True, anchor="end")
f.text(290, 214, "cardinality = 4", size=9.5, color=AMBER, anchor="end")
f.text(150, 240, "degree = 3 | NULL = unknown value", size=10, color=RED, bold=True)
f.text(150, 258, "domain of dept_id: whole numbers", size=9.5, color=SLATE)
```

```svgfig label="3.1" caption="The family of keys. A super key is any set of attributes that identifies a tuple uniquely, so it may contain extra attributes. A candidate key is a minimal super key (no attribute can be removed). One candidate key is chosen as the primary key; the others are alternate keys. A foreign key is an attribute in one table that must match a primary key value in another table. In Student(sid, name, email, dept_id): sid and email are candidate keys, sid is the primary key, email is an alternate key and dept_id is a foreign key."
f = Fig(580, 230)
f.box(10, 10, 560, 210, "", fill=SOFT, stroke=SLATE, sw=1.2)
f.text(290, 26, "Super keys: {sid}, {email}, {sid, name}, {sid, email}, {sid, name, dept_id} ...", size=10, color=SLATE, bold=True)
f.box(40, 48, 360, 120, "", fill=BLUE, stroke=NAVY, sw=1.6)
f.text(220, 64, "Candidate keys (minimal super keys)", size=10.5, color=NAVY, bold=True)
f.box(60, 82, 140, 60, "Primary key\n{sid}", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(240, 82, 140, 60, "Alternate key\n{email}", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(425, 82, 130, 60, "Foreign key\ndept_id", fill=ROSE, stroke=RED, size=11, bold=True)
f.text(220, 156, "chosen: never NULL, never changes", size=9.5, color=SLATE)
f.arrow([(490, 142), (490, 190), (330, 190)], color=RED, sw=1.4)
f.box(220, 176, 110, 30, "Department.dept_id", fill=SOFT, stroke=RED, size=9.5, bold=True)
f.text(500, 206, "refers to", size=9, color=RED, bold=True)
```

```svgfig label="3.2" caption="A schema diagram for the sample database. Each box is a table with its primary key underlined by a bar, and each arrow runs from a foreign key to the primary key it references. Referential integrity says that every value of a foreign key must either be NULL or exist in the referenced key. Student row (4, Gita, NULL) is therefore legal, while Student row (5, Mina, 99) would be rejected because no department has dept_id 99."
f = Fig(580, 210)
def tab(x, y, w, nm, cols, key):
    f.box(x, y, w, 26, nm, fill=NAVY, stroke=NAVY, color="#ffffff", size=10.5, bold=True, r=0)
    for i, c in enumerate(cols):
        f.box(x, y + 26 + i * 22, w, 22, c, fill=BLUE if c in key else SOFT, stroke=NAVY, size=10, r=0, bold=(c in key))
tab(10, 30, 130, "Department", ["dept_id", "dept_name"], ["dept_id"])
tab(225, 30, 130, "Student", ["sid", "name", "dept_id"], ["sid"])
tab(440, 30, 130, "Enrollment", ["sid", "cid", "marks"], ["sid", "cid"])
f.arrow([(225, 98), (140, 80)], color=RED, sw=1.6, label="FK", lpos=(182, 80), lsize=9)
f.arrow([(440, 76), (355, 76)], color=RED, sw=1.6, label="FK sid", lpos=(397, 64), lsize=9)
f.box(10, 150, 560, 46, "Insert Enrollment(9, C1, 70): rejected, there is no student 9\nDelete Department 10: rejected, or cascade, or set NULL (designer's choice)", fill=ROSE, stroke=RED, size=10, bold=True)
```

```svgfig label="3.3" caption="The four joins on the sample data. The inner (natural) join keeps only matching rows, so Gita (no department) and BBS (no student) vanish. The left outer join keeps every Student row and pads with NULL where there is no match. The right outer join keeps every Department row, and the full outer join keeps both unmatched rows. The counts are 3, 4, 4 and 5 rows."
f = Fig(580, 230)
def box4(x, title, rows, st, fl):
    f.text(x + 66, 12, title, size=10.5, color=st, bold=True)
    for i, r in enumerate(rows):
        f.box(x, 22 + i * 24, 132, 24, r, fill=fl if r else SOFT, stroke=st, size=9, r=0)
inner = ["Sita | BCA", "Ram | BCA", "Hari | BIT"]
box4(5, "Inner join (3)", inner, NAVY, BLUE)
box4(150, "Left outer (4)", inner + ["Gita | NULL"], TEAL, MINT)
box4(295, "Right outer (4)", inner + ["NULL | BBS"], AMBER, SAND)
box4(440, "Full outer (5)", inner + ["Gita | NULL", "NULL | BBS"], RED, ROSE)
f.text(290, 170, "Student(sid, name, dept_id)  JOIN  Department(dept_id, dept_name)  ON dept_id", size=10, color=SLATE, bold=True)
f.text(290, 192, "Rows shown as  name | dept_name.   Matching rows: 3 of 4 students, 3 of 3 used departments.", size=9.5, color=SLATE)
f.text(290, 212, "Outer joins are the safe choice when you must not lose rows from one side.", size=9.5, color=TEAL, bold=True)
```

```svgfig label="3.4" caption="Two equivalent query trees for the names of students who scored above 80. The left tree joins first and selects later, so the join works on every enrolment row. The right tree pushes the selection down to the Enrollment table, so only two rows (Sita 85, Hari 91) reach the join. Both give the same answer, Sita and Hari, but the second does less work. Choosing such equivalent forms is the job of the query optimiser (Unit 8)."
f = Fig(580, 250)
f.text(145, 12, "Join first", size=11, color=RED, bold=True)
f.box(80, 24, 130, 28, "project name", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(80, 74, 130, 28, "select marks > 80", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(80, 124, 130, 28, "Student JOIN Enrollment", fill=ROSE, stroke=RED, size=9, bold=True)
f.box(30, 190, 90, 28, "Student (4)", fill=SOFT, stroke=SLATE, size=10, bold=True)
f.box(170, 190, 100, 28, "Enrollment (4)", fill=SOFT, stroke=SLATE, size=10, bold=True)
for a, b in [((145, 52), (145, 74)), ((145, 102), (145, 124)), ((120, 152), (75, 190)), ((170, 152), (220, 190))]:
    f.line(a[0], a[1], b[0], b[1], color=SLATE, sw=1.4)
f.text(310, 138, "join sees 4 rows", size=9.5, color=RED, bold=True)
f.text(435, 12, "Select first (optimised)", size=11, color=TEAL, bold=True)
f.box(370, 24, 130, 28, "project name", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(370, 74, 130, 28, "Student JOIN", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(320, 124, 100, 28, "Student (4)", fill=SOFT, stroke=SLATE, size=10, bold=True)
f.box(450, 124, 120, 28, "select marks > 80", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(450, 190, 120, 28, "Enrollment (4)", fill=SOFT, stroke=SLATE, size=10, bold=True)
for a, b in [((435, 52), (435, 74)), ((410, 102), (370, 124)), ((460, 102), (510, 124)), ((510, 152), (510, 190))]:
    f.line(a[0], a[1], b[0], b[1], color=SLATE, sw=1.4)
f.text(420, 175, "join sees 2 rows", size=9.5, color=TEAL, bold=True)
f.text(290, 242, "same result: Sita, Hari", size=10.5, color=NAVY, bold=True)
```

A key is a promise about the whole world, not a fact read from a handful of rows. The first plate shows why, using a sample of six students and a brute-force search over every set of attributes; the second uses a real PostgreSQL run to count the rows that come out of each relational-algebra operator.

```photogrid label="3.2" cols="2" ratio="1.6" caption="Keys are chosen by meaning. (a) A specimen of Nepal's National Identity Card: the card number is unique to one citizen, so it is a natural candidate key, whereas a name or a date of birth is not. (b) All 63 non-empty subsets of six attributes of a Student table (sid, citizen_no, email, name, dept_id, phone) tested on six sample rows. The grid shows how many subsets of each size are superkeys (teal) and which are minimal, the candidate keys (amber outline). The search finds 60 superkeys, but (name, dept_id) and two other pairs are only accidents of this small sample: a design must rely on the meaning of the data, not on the rows seen so far."
@ photo id="bca202/nid" cap="Specimen of the Nepal National Identity Card"
fit 1.6
focus 0.5 0.5
@ svg cap="Superkey search over all 63 attribute subsets"
from itertools import combinations
attrs = ["sid", "citizen_no", "email", "name", "dept_id", "phone"]
rows = [(1, "27-01-71-00123", "sita@x.np", "Sita", 10, "9841000001"), (2, "27-01-72-00456", "ram@x.np", "Ram", 10, "9841000002"), (3, "01-02-70-00789", "hari@x.np", "Hari", 20, "9841000002"), (4, "27-01-73-00111", "gita@x.np", "Sita", 20, "9841000004"), (5, "12-03-74-00222", "mina@x.np", "Mina", 10, "9841000005"), (6, "27-01-74-00333", "anil@x.np", "Anil", 30, "9841000006")]
def uniq(S):
    ix = [attrs.index(a) for a in S]
    return len({tuple(r[i] for i in ix) for r in rows}) == len(rows)
allsub = [S for n in range(1, 7) for S in combinations(attrs, n)]
sup = [S for S in allsub if uniq(S)]
cand = [S for S in sup if not any(set(T) < set(S) for T in sup)]
assert len(allsub) == 63
nsup, ncand = len(sup), len(cand)
single = [S[0] for S in cand if len(S) == 1]
print("superkeys", nsup, "candidates", ncand, single)
f = Fig(300, 250)
f.text(150, 12, "%d of 63 subsets are superkeys, %d are candidate keys" % (nsup, ncand), size=10, color=NAVY, bold=True)
for n in range(1, 7):
    S_n = [S for S in allsub if len(S) == n]
    y = 28 + (n - 1) * 24
    f.text(16, y + 8, "size %d" % n, size=9.5, color=SLATE, bold=True, anchor="start")
    for i, S in enumerate(S_n):
        isc = S in cand
        f.box(64 + i * 11.5, y, 10, 16, "", fill=(TEAL if S in sup else "#e2e8f0"), stroke=(AMBER if isc else "#ffffff"), sw=(2.2 if isc else 0.5), r=1)
f.text(8, 184, "single-attribute candidate keys: " + ", ".join(single), size=9.5, color=TEAL, bold=True, anchor="start")
f.text(8, 198, "pairs that are luck of the sample:\n" + ", ".join("(%s, %s)" % S for S in cand if len(S) == 2), size=9, color=RED, bold=True, anchor="start")
f.box(8, 214, 284, 30, "add one more student named Sita in dept 10 and\nthose pair keys would stop working", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

```photogrid label="3.3" cols="2" ratio="1.2" caption="Operators change cardinality. (a) A Devanagari vehicle number plate: the letters and digits of the plate together identify one vehicle, a composite key, because no single part is unique. (b) Row counts measured on real PostgreSQL 15 for a Student table of 40 rows (5 with no department) and a Department table of 3 rows. Selection keeps 20 rows, projection with duplicates removed keeps 3 distinct department ids, the Cartesian product gives 40 x 3 = 120 rows, the natural join keeps 35 (the 5 students with a NULL department have no partner), the left outer join keeps all 40, and division finds the 10 students who study all three subjects."
@ photo id="bca202/nplate" cap="Vehicle number plate in Devanagari"
fit 1.2
focus 0.5 0.5
@ svg cap="Cardinality of each operator (real run)"
meas = [("Student", 40), ("Department", 3), ("select dept=10", 20), ("project dept_id", 3), ("student x dept", 120), ("natural join", 35), ("left outer join", 40), ("division (all 3)", 10)]
d = dict(meas)
assert d["student x dept"] == d["Student"] * d["Department"] and d["Student"] - d["natural join"] == 5
f = Fig(300, 244)
f.text(150, 11, "rows returned (PostgreSQL 15, 40-row Student)", size=10, color=NAVY, bold=True)
for i, (k, v) in enumerate(meas):
    y = 24 + i * 26
    w = 130 * v / 120
    col = RED if k == "student x dept" else (AMBER if k == "natural join" else TEAL)
    f.text(6, y + 9, k, size=9.5, color=SLATE, bold=True, anchor="start")
    f.box(112, y, max(w, 2), 17, "", fill=col, stroke=col, r=2)
    f.text(112 + max(w, 2) + 5, y + 9, str(v), size=10, color=col, bold=True, anchor="start")
f.text(150, 238, "join 35 = 40 - 5 students with NULL department", size=9.5, color=AMBER, bold=True)
```

### 3.5.1 Eight advantages of the relational model

1. **It is simple.** Everything is a table of rows and columns, a picture that a school student already understands. A Nepali college clerk can read a Student table without any training in computer science. This simplicity is a main reason why the model replaced older tree and network models.
2. **It has a strong mathematical base.** Relations are sets, and relational algebra and calculus give exact rules for what a query means. Because of this, two different-looking queries can be proved equal, and an optimiser can rewrite them safely. Reliable behaviour comes from this foundation.
3. **Data independence is high.** Programs name tables and columns and never follow physical pointers. The DBA can add an index or move files and no application needs to change. This saves large amounts of maintenance work.
4. **It uses a declarative language.** In SQL you say what you want, such as the names of students above 80 marks, and the system decides how to get it. You do not write loops over files. A short query replaces a long program.
5. **Integrity is built in.** Primary keys, foreign keys, NOT NULL and CHECK rules are declared once with the table. The DBMS rejects a Student row that points to a missing department. Clean data results without extra code in every program.
6. **Relationships are flexible.** Tables are linked by matching values, so new links can be made at query time, for example joining Student with Enrollment by sid. No one has to plan every path in advance, as in network databases. Ad-hoc questions from managers can be answered at once.
7. **Normalisation gives sound design.** Theory of functional dependencies tells us how to split tables to remove redundancy and update anomalies (Unit 4). A bank can store each customer once and link accounts to the customer. Storage is saved and updates stay consistent.
8. **A huge ecosystem exists.** MySQL, PostgreSQL, Oracle, SQL Server and SQLite all follow the same model and mostly the same SQL. Skills learned in this course apply to a bank, to a government portal and to a mobile app. Tools for backup, reporting and security are plentiful.

## Formula and fact sheet

- Candidate key = minimal super key; primary key chosen from candidates; foreign key references a primary key.
- Entity integrity: PK ≠ NULL. Referential integrity: FK matches a PK or is NULL.
- |R × S| = |R|·|S|. Natural join = product + equality on common attributes + project.
- Fundamental operators: σ, π, ∪, −, ×, ρ.

## Chapter summary

- A relation is a set of unique tuples over atomic domains; keys identify tuples and link tables.
- Integrity rules keep data valid across tables.
- Relational algebra composes select, project, product, set operations and joins to express any query; outer joins preserve unmatched rows.

## Practice

1. Define relation, tuple, attribute, degree, cardinality, domain.
2. Differentiate super, candidate, primary and foreign keys with Student(sid, email, name).
3. State entity and referential integrity; give a violation of each.
4. Using the sample data, evaluate π_dept_name(Department ⋈ Student) and Department − π_dept_id(Student) (rename as needed).
5. Write relational algebra for "names of students who scored below 70 in any course".
6. What is the difference between ⋈ and ×?
7. What does a left outer join give that a natural join does not?
8. How many super keys does R(A, B, C) have if A is the only candidate key?

::: note Answers and worked solutions
**1.** Relation: a set of tuples over a schema; tuple: a row; attribute: a column; degree: number of columns; cardinality: number of rows; domain: set of legal values.
**2.** Super: {sid}, {email}, {sid, name}, … Candidate: {sid}, {email}. Primary: say {sid}. Foreign key: an attribute of another table that refers to Student.sid.
**3.** Entity: PK not NULL (inserting a row with sid = NULL violates it). Referential: FK matches an existing PK (a student with dept_id 99 when no such department exists).
**4.** Department ⋈ Student → BCA, BCA, BIT, so π_dept_name = {BCA, BIT}. Department − π_dept_id(Student) = departments with no students (compare on dept_id) = (30, BBS).
**5.** π_name(Student ⋈ σ_marks<70(Enrollment)) → Ram (64).
**6.** × pairs every row with every row; ⋈ keeps only pairs that agree on the common attributes and removes the duplicate column.
**7.** The rows of the left relation with no match, padded with NULLs (Gita).
**8.** Any attribute set containing A: 2² = **4** ({A}, {A,B}, {A,C}, {A,B,C}).
:::

## Model answers (5 and 10 marks)

**Q1 (5 marks). Explain the different types of keys in the relational model with examples.**

*Introduction.* A key is an attribute or set of attributes that identifies tuples. Keys make the relational model work because rows have no order and cannot be found by position. Figure 3.1 shows how the types are related, using Student(sid, name, email, dept_id).

1. **Super key.** Any set of attributes that identifies a tuple uniquely. {sid}, {email}, {sid, name} and {sid, name, dept_id} are all super keys; some contain unnecessary attributes.
2. **Candidate key.** A minimal super key, one from which no attribute can be removed. Here {sid} and {email} are candidate keys, but {sid, name} is not because name can be dropped.
3. **Primary key.** The candidate key chosen by the designer to identify tuples. It can never be NULL and should not change, so sid is a good choice.
4. **Alternate key.** A candidate key that was not chosen, here email. It is usually declared UNIQUE.
5. **Composite key.** A key made of more than one attribute. In Enrollment(sid, cid, marks) the pair (sid, cid) is the primary key because one student can take many courses and one course has many students.
6. **Foreign key.** An attribute of one table that refers to the primary key of another, such as dept_id in Student referring to Department. It creates the link between tables and enforces referential integrity.

*Conclusion.* A table has many super keys and candidate keys, one primary key and as many foreign keys as it has links to other tables.

**Q2 (5 marks). What are integrity constraints? Explain the types with examples.**

*Introduction.* Integrity constraints are rules declared in the schema that the DBMS checks on every insert, update and delete. They keep the data correct and consistent without relying on every programmer. Figure 3.2 gives a sample schema.

1. **Domain constraint.** Each value must belong to the domain of its column: a data type plus rules such as `CHECK (marks BETWEEN 0 AND 100)`. A mark of 150 is rejected.
2. **Key constraint.** The values of a candidate key must be unique. Two students cannot have the same sid.
3. **Entity integrity.** No attribute of a primary key may be NULL, because a row that cannot be identified is not a real entity. Enrollment cannot have a row with sid NULL.
4. **Referential integrity.** A foreign key value must be NULL or must match an existing primary key value. Enrollment(9, C1, 70) is rejected when student 9 does not exist, but Student(4, Gita, NULL) is allowed because NULL means no department yet.
5. **NOT NULL and UNIQUE.** These force a value to be present or different from all others, for example for a phone number.
6. **Actions on delete and update.** When a referenced row is deleted the designer chooses `RESTRICT` (refuse), `CASCADE` (delete dependent rows) or `SET NULL`.

*Example.* Deleting department 10 with `ON DELETE RESTRICT` fails while Sita and Ram still belong to it.

*Conclusion.* Declared constraints guard the database at one central place, so wrong data is stopped before it enters.

**Q3 (10 marks). Explain the operators of relational algebra with examples. Use Student(sid, name, dept_id): (1, Sita, 10), (2, Ram, 10), (3, Hari, 20), (4, Gita, NULL); Department(dept_id, dept_name): (10, BCA), (20, BIT), (30, BBS); Enrollment(sid, cid, marks): (1, C1, 85), (1, C2, 72), (2, C1, 64), (3, C2, 91).**

*Introduction.* Relational algebra is a procedural query language whose operators take one or two relations and return a relation, so operators can be nested. It is the theory that SQL is built on and that the optimiser (Figure 3.4) uses to rewrite queries.

*Fundamental operators.*
1. **Select, σ.** Chooses rows. σ_dept_id=10(Student) gives (1, Sita, 10) and (2, Ram, 10).
2. **Project, π.** Chooses columns and removes duplicates. π_name(Student) gives Sita, Ram, Hari, Gita.
3. **Union, ∪.** Rows in either relation; the relations must be union-compatible, with the same number and types of attributes.
4. **Set difference, −.** Rows in the first but not the second. π_sid(Student) − π_sid(Enrollment) gives {4}: Gita has no enrolment.
5. **Cartesian product, ×.** Every row of one with every row of the other. Student × Department has 4 × 3 = 12 rows.
6. **Rename, ρ.** Gives a new name to a relation or attribute, which is necessary for self-joins.

*Derived operators.*
7. **Intersection** R ∩ S = R − (R − S).
8. **Natural join, ⋈.** A product followed by selection on equal common attributes with the duplicate column removed. Student ⋈ Department gives three rows (Figure 3.3); Gita and BBS disappear.
9. **Outer joins.** The left outer join also keeps (4, Gita, NULL, NULL); the full outer join keeps BBS as well, with NULLs.
10. **Division, ÷.** Finds values related to all rows of another relation: π_sid,cid(Enrollment) ÷ {C1, C2} gives sid 1, because only Sita took both courses.

*Combined query.* The names of students scoring above 80 are π_name(σ_marks>80(Student ⋈ Enrollment)) = Sita (85) and Hari (91).

| Operator | Symbol | Result for the sample data |
|---|---|---|
| Select | σ | 2 rows |
| Project | π | 4 names |
| Natural join | ⋈ | 3 rows |
| Product | × | 12 rows |
| Division | ÷ | sid 1 |

*Conclusion.* Six fundamental operators are enough to express any relational query, and the derived operators make queries shorter. Pushing selections before joins gives the same answer with less work.
