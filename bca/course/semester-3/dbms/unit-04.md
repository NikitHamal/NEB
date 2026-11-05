---
subject: Database Management System
grade: BCA Semester 3
unit: 4
title: Database Normalization
hours: 4
area: BCA 202 · Database Management System · Unit 4
---

**Normalization** is the process of organising tables to remove redundancy and the update problems that come with it. It is driven by **functional dependencies** and carried out by decomposing tables into normal forms.

::: key What this unit gives you
- Why redundancy hurts: insertion, deletion and update anomalies.
- Functional dependencies, closure and finding candidate keys.
- 1NF, 2NF, 3NF, BCNF and 4NF with worked decompositions.
:::

## 4.1 Definition and importance

Consider one wide table `StudentCourse(sid, name, dept, cid, title, marks)` storing the student's name and department on every enrolment row.

- **Update anomaly:** Sita's department appears in many rows; change it in one and the data is inconsistent.
- **Insertion anomaly:** a new student who has not enrolled cannot be added (cid would be NULL, part of the key).
- **Deletion anomaly:** deleting Sita's only enrolment also deletes the fact that she exists.

Normalization removes these by splitting the table so each fact is stored once. A good decomposition is **lossless** (the original can be rebuilt by joining) and ideally **dependency preserving**.

## 4.2 Functional dependencies

**X → Y** (X determines Y) holds in a relation if any two tuples that agree on X also agree on Y. Examples: sid → name; (sid, cid) → marks; cid → title.

**Armstrong's axioms:** *Reflexivity* (if Y ⊆ X then X → Y); *Augmentation* (X → Y ⇒ XZ → YZ); *Transitivity* (X → Y, Y → Z ⇒ X → Z). Derived: union (X → Y, X → Z ⇒ X → YZ), decomposition, pseudo-transitivity.

A **trivial** FD has Y ⊆ X. The **closure X⁺** is the set of attributes determined by X, computed by repeatedly adding the right side of every FD whose left side is already inside. X is a **super key** iff X⁺ is all attributes; a **candidate key** if additionally minimal.

::: example Worked example: closure and keys
R(A, B, C, D, E) with F = {A → B, BC → D, D → E}. Compute (AC)⁺: start {A, C}; A → B adds B → {A, B, C}; BC → D adds D → {A, B, C, D}; D → E adds E → {A, B, C, D, E} = all. AC is a super key; A⁺ = {A, B} and C⁺ = {C} are not, so **AC is a candidate key** (the only one, since A and C appear on no right side and so must be in every key).
:::

## 4.3 First normal form (1NF)

Every attribute holds a single **atomic** value; no repeating groups. A table with `phone = '9801, 9802'` violates 1NF; fix by one row per phone value (or a separate phone table).

## 4.4 Second normal form (2NF)

A table is in 2NF if it is in 1NF and **no non-key attribute depends on part of a composite key** (no *partial dependency*). Only tables with composite keys can violate it.

::: example Worked example: to 2NF
`Enrollment(sid, cid, name, title, marks)` with key (sid, cid), FDs: sid → name; cid → title; (sid, cid) → marks. `name` and `title` depend on only part of the key. Decompose: **Student(sid, name)**, **Course(cid, title)**, **Enrollment(sid, cid, marks)**.
:::

## 4.5 Third normal form (3NF)

A table is in 3NF if it is in 2NF and **no non-key attribute depends transitively on the key** (non-key → non-key). Formally, for every non-trivial X → A: X is a super key, **or** A is a prime attribute (part of some candidate key).

::: example Worked example: to 3NF
`Student(sid, name, dept_id, dept_name)`, key sid; FDs: sid → dept_id, dept_id → dept_name. So sid → dept_name transitively. Decompose: **Student(sid, name, dept_id)** and **Department(dept_id, dept_name)**. The join on dept_id restores the original (lossless) and both FDs are preserved.
:::

## 4.6 Boyce–Codd normal form (BCNF)

A table is in BCNF if for **every** non-trivial FD X → Y, **X is a super key**. BCNF is stricter than 3NF: it removes the "prime attribute" loophole. Every BCNF table is in 3NF; the converse fails only when a table has overlapping composite candidate keys.

::: example Worked example: 3NF but not BCNF
`Teaching(student, subject, teacher)`: each teacher teaches one subject (teacher → subject); a student has one teacher per subject ((student, subject) → teacher). Candidate keys: (student, subject) and (student, teacher). The FD teacher → subject has a left side that is **not a super key**, but `subject` is prime, so the table is in 3NF yet not BCNF. Decompose into **TeacherSubject(teacher, subject)** and **StudentTeacher(student, teacher)**. It is lossless, but the FD (student, subject) → teacher is no longer enforceable within one table: BCNF may sacrifice dependency preservation, which is why 3NF is often the practical target.
:::

## 4.7 Fourth normal form (4NF) — multivalued dependencies

A **multivalued dependency** X ↠ Y holds when, for each X value, the set of Y values is independent of the other attributes. A table is in **4NF** if it is in BCNF and every non-trivial MVD X ↠ Y has X as a super key.

::: example Worked example: to 4NF
`CourseInfo(course, teacher, book)`: a course has several teachers and several books, independently. Storing all combinations forces rows such as (DBMS, Ram, Korth), (DBMS, Ram, Elmasri), (DBMS, Hari, Korth), (DBMS, Hari, Elmasri): course ↠ teacher and course ↠ book, but course is not a key. Decompose: **CourseTeacher(course, teacher)** and **CourseBook(course, book)**; redundancy disappears.
:::

## 4.8 Summary of the normal forms

| Form | Removes | Rule |
|---|---|---|
| 1NF | repeating groups, multi-valued cells | atomic values |
| 2NF | partial dependency | non-key depends on the **whole** key |
| 3NF | transitive dependency | non-key depends on **nothing but** the key |
| BCNF | every dependency on a non-super-key | every determinant is a super key |
| 4NF | non-trivial multivalued dependency | MVD determinants are super keys |

"The key, the whole key, and nothing but the key." **Denormalization** (deliberately re-introducing redundancy) is sometimes used in reporting systems for speed, at the price of the anomalies above.

## Formula and fact sheet

- X⁺ = closure; X is a super key iff X⁺ = all attributes.
- Armstrong: reflexivity, augmentation, transitivity.
- 2NF: no partial dependency. 3NF: no transitive dependency (or RHS prime). BCNF: LHS always a super key. 4NF: no non-trivial MVD.
- A lossless decomposition of R into R₁, R₂ needs R₁ ∩ R₂ → R₁ or R₂.

## Chapter summary

- Anomalies come from redundancy; normalization removes it by decomposition.
- Closures of attribute sets find keys.
- 1NF (atomic) → 2NF (no partial) → 3NF (no transitive) → BCNF (all determinants keys) → 4NF (no MVD).

## Practice

1. Define normalization; explain the three anomalies with a table of your own.
2. For R(A, B, C, D) with A → B, B → C, C → D find A⁺, B⁺ and the candidate key.
3. Normalize Order(oid, date, cid, cname, pid, pname, qty) with key (oid, pid) and FDs oid → date, cid; cid → cname; pid → pname.
4. Why is every 2NF violation about a composite key?
5. Differentiate 3NF and BCNF with an example.
6. State the 4NF rule and give an example of a multivalued dependency.
7. Check whether the decomposition of R(A, B, C) with B → C into R₁(A, B), R₂(B, C) is lossless.

::: note Answers and worked solutions
**1.** Normalization organises tables to remove redundancy using FDs. Anomalies (see 4.1): update (inconsistency), insertion (cannot add a fact without another), deletion (losing one fact loses another).
**2.** A⁺ = {A, B, C, D} (A→B, B→C, C→D); B⁺ = {B, C, D}. Candidate key: **A**.
**3.** 1NF already. Partial dependencies: oid → date, cid; pid → pname. Result: **Orders(oid, date, cid)**, **Product(pid, pname)**, **OrderItem(oid, pid, qty)**. Transitive: cid → cname: **Customer(cid, cname)**, and Orders keeps cid as FK. Final 3NF set: Customer, Orders, Product, OrderItem.
**4.** A partial dependency is a dependency on *part* of a key; a single-attribute key has no proper part.
**5.** 3NF allows X → A when A is prime; BCNF does not. Example: Teaching(student, subject, teacher) in 4.6.
**6.** 4NF: BCNF plus every non-trivial MVD has a super-key left side. Example: course ↠ teacher with course ↠ book independent.
**7.** R₁ ∩ R₂ = {B}, and B → C means B is a key of R₂(B, C). So the join on B reproduces R exactly: **lossless**.
:::
