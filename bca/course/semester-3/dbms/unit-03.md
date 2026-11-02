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
