---
subject: Database Management System
grade: BCA Semester 3
unit: 6
title: Manipulating and Querying Data
hours: 8
area: BCA 202 · Database Management System · Unit 6
---

This unit covers the **DML** core of SQL: `INSERT`, `SELECT` with filtering, ordering, grouping, joins and subqueries, `UPDATE`, `DELETE`, and views. Everything is demonstrated on the college database from Units 3 and 5, and every output below was produced by running the statements.

::: key What this unit gives you
- `INSERT`; `SELECT … FROM … WHERE`, `ORDER BY`, `GROUP BY … HAVING`, aggregates.
- Inner, outer and cross joins; nested and correlated subqueries; set operators.
- `UPDATE`, `DELETE`; creating, altering and dropping views.
:::

## 6.1 The sample database

```sql
CREATE TABLE department (dept_id INT PRIMARY KEY, dept_name VARCHAR(40));
CREATE TABLE student (sid INT PRIMARY KEY, name VARCHAR(50), dept_id INT, city VARCHAR(30));
CREATE TABLE course (cid CHAR(2) PRIMARY KEY, title VARCHAR(40), credits INT);
CREATE TABLE enrollment (sid INT, cid CHAR(2), marks INT, PRIMARY KEY (sid, cid));
INSERT INTO department VALUES (10, 'BCA'), (20, 'BIT'), (30, 'BBS');
INSERT INTO student VALUES (1, 'Sita', 10, 'Kathmandu'), (2, 'Ram', 10, 'Pokhara'),
                           (3, 'Hari', 20, 'Kathmandu'), (4, 'Gita', NULL, 'Biratnagar');
INSERT INTO course VALUES ('C1', 'DBMS', 3), ('C2', 'DSA', 3), ('C3', 'Web Technology', 3);
INSERT INTO enrollment VALUES (1, 'C1', 85), (1, 'C2', 72), (2, 'C1', 64), (3, 'C2', 91);
SELECT * FROM student;
```
```output
 sid | name | dept_id |    city    
-----+------+---------+------------
   1 | Sita |      10 | Kathmandu
   2 | Ram  |      10 | Pokhara
   3 | Hari |      20 | Kathmandu
   4 | Gita |         | Biratnagar
(4 rows)
```

`INSERT INTO t VALUES (…), (…);` adds rows in column order; `INSERT INTO t (col, …) VALUES (…)` names the columns (unlisted columns get `DEFAULT` or `NULL`); `INSERT INTO t SELECT …` copies query results.

## 6.2 SELECT, FROM and WHERE

`SELECT [DISTINCT] columns FROM table [WHERE condition];` The logical order of evaluation is **FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY**, which explains why a column alias cannot be used in `WHERE`.

| Condition | Meaning |
|---|---|
| `=  <>  <  >  <=  >=` | comparison |
| `AND  OR  NOT` | logic |
| `BETWEEN a AND b` | inclusive range |
| `IN (a, b, …)` | membership |
| `LIKE 'pattern'` | `%` any string, `_` one character |
| `IS NULL` / `IS NOT NULL` | NULL test (`= NULL` never works) |

```sql
SELECT name, city FROM student WHERE city = 'Kathmandu';
SELECT DISTINCT city FROM student ORDER BY city;
SELECT name FROM student WHERE name LIKE '_i%' OR dept_id IS NULL;
SELECT sid, cid, marks FROM enrollment WHERE marks BETWEEN 70 AND 90 AND cid IN ('C1', 'C2');
SELECT name FROM student WHERE dept_id <> 10;
```
```output
 name |   city    
------+-----------
 Sita | Kathmandu
 Hari | Kathmandu
(2 rows)

    city    
------------
 Biratnagar
 Kathmandu
 Pokhara
(3 rows)

 name 
------
 Sita
 Gita
(2 rows)

 sid | cid | marks 
-----+-----+-------
   1 | C1  |    85
   1 | C2  |    72
(2 rows)

 name 
------
 Hari
(1 row)
```

The last query illustrates **three-valued logic**: Gita (dept_id NULL) is missing, because `NULL <> 10` is *unknown*, not true. Test NULL with `IS NULL`.

## 6.3 ORDER BY, aggregates, GROUP BY and HAVING

`ORDER BY col [ASC|DESC]` sorts the result. **Aggregates** collapse rows: `COUNT(*)` (rows), `COUNT(col)` (non-NULL values), `SUM`, `AVG`, `MIN`, `MAX`; they ignore NULLs (except `COUNT(*)`). `GROUP BY` forms groups; `HAVING` filters **groups** (while `WHERE` filters rows *before* grouping). Every selected column must be grouped or aggregated.

```sql
SELECT count(*) AS rows, count(dept_id) AS with_dept FROM student;
SELECT cid, count(*) AS students, round(avg(marks), 1) AS avg_marks, max(marks) AS best
FROM enrollment GROUP BY cid ORDER BY cid;
SELECT sid, sum(marks) AS total FROM enrollment GROUP BY sid HAVING sum(marks) > 100 ORDER BY total DESC;
SELECT name, marks FROM student s JOIN enrollment e ON s.sid = e.sid WHERE cid = 'C2' ORDER BY marks DESC;
```
```output
 rows | with_dept 
------+-----------
    4 |         3
(1 row)

 cid | students | avg_marks | best 
-----+----------+-----------+------
 C1  |        2 |      74.5 |   85
 C2  |        2 |      81.5 |   91
(2 rows)

 sid | total 
-----+-------
   1 |   157
(1 row)

 name | marks 
------+-------
 Hari |    91
 Sita |    72
(2 rows)
```

## 6.4 Joins

| Join | Rows returned |
|---|---|
| `INNER JOIN … ON` | only matching pairs |
| `LEFT [OUTER] JOIN` | all left rows; NULLs where there is no match |
| `RIGHT [OUTER] JOIN` | all right rows |
| `FULL [OUTER] JOIN` | all rows of both |
| `CROSS JOIN` | Cartesian product |

```sql
SELECT s.name, d.dept_name FROM student s INNER JOIN department d ON s.dept_id = d.dept_id ORDER BY s.sid;
SELECT s.name, d.dept_name FROM student s LEFT JOIN department d ON s.dept_id = d.dept_id ORDER BY s.sid;
SELECT s.name, d.dept_name FROM student s RIGHT JOIN department d ON s.dept_id = d.dept_id ORDER BY d.dept_id, s.sid;
SELECT count(*) AS cross_rows FROM student CROSS JOIN department;
SELECT s.name, c.title, e.marks
FROM student s JOIN enrollment e ON s.sid = e.sid JOIN course c ON c.cid = e.cid
ORDER BY s.name, c.title;
```
```output
 name | dept_name 
------+-----------
 Sita | BCA
 Ram  | BCA
 Hari | BIT
(3 rows)

 name | dept_name 
------+-----------
 Sita | BCA
 Ram  | BCA
 Hari | BIT
 Gita | 
(4 rows)

 name | dept_name 
------+-----------
 Sita | BCA
 Ram  | BCA
 Hari | BIT
      | BBS
(4 rows)

 cross_rows 
------------
         12
(1 row)

 name | title | marks 
------+-------+-------
 Hari | DSA   |    91
 Ram  | DBMS  |    64
 Sita | DBMS  |    85
 Sita | DSA   |    72
(4 rows)
```

The left join shows Gita (no department); the right join shows BBS (no students); the cross join returns 4 × 3 = 12 rows. A three-table join is just two joins chained.

## 6.5 Nested queries (subqueries)

A **subquery** is a `SELECT` inside another. A **scalar** subquery returns one value; `IN` tests membership in a list; `EXISTS` tests for any row; `ANY`/`ALL` compare with a set. A **correlated** subquery refers to the outer row and is re-evaluated for each of its rows.

```sql
SELECT name FROM student WHERE sid IN (SELECT sid FROM enrollment WHERE marks > 80);
SELECT name FROM student s WHERE NOT EXISTS (SELECT 1 FROM enrollment e WHERE e.sid = s.sid);
SELECT sid, cid, marks FROM enrollment WHERE marks > (SELECT avg(marks) FROM enrollment);
SELECT sid, cid, marks FROM enrollment e1
WHERE marks = (SELECT max(marks) FROM enrollment e2 WHERE e2.cid = e1.cid) ORDER BY cid;
SELECT title FROM course WHERE cid NOT IN (SELECT cid FROM enrollment);
```
```output
 name 
------
 Sita
 Hari
(2 rows)

 name 
------
 Gita
(1 row)

 sid | cid | marks 
-----+-----+-------
   1 | C1  |    85
   3 | C2  |    91
(2 rows)

 sid | cid | marks 
-----+-----+-------
   1 | C1  |    85
   3 | C2  |    91
(2 rows)

     title      
----------------
 Web Technology
(1 row)
```

The correlated query finds the **top mark in each course**. `NOT IN` is dangerous if the subquery can return NULL (the whole condition becomes unknown); `NOT EXISTS` is the safe form.

**Set operators** combine compatible queries: `UNION` (removes duplicates; `UNION ALL` keeps them), `INTERSECT`, `EXCEPT` (`MINUS` in Oracle).

```sql
SELECT sid FROM student EXCEPT SELECT sid FROM enrollment;
SELECT cid FROM enrollment WHERE marks > 80 UNION SELECT cid FROM enrollment WHERE marks < 70 ORDER BY cid;
```
```output
 sid 
-----
   4
(1 row)

 cid 
-----
 C1
 C2
(2 rows)
```

## 6.6 UPDATE and DELETE

`UPDATE t SET col = expr [, …] [WHERE condition];` and `DELETE FROM t [WHERE condition];`. **Without `WHERE` every row is changed or removed.** Both can use subqueries in their conditions.

```sql
UPDATE enrollment SET marks = marks + 5 WHERE cid = 'C1' AND marks < 70;
UPDATE student SET city = 'Lalitpur', dept_id = 30 WHERE name = 'Gita';
DELETE FROM enrollment WHERE marks < 70 OR sid NOT IN (SELECT sid FROM student);
SELECT s.name, s.city, s.dept_id FROM student s ORDER BY sid;
SELECT * FROM enrollment ORDER BY sid, cid;
```
```output
 name |   city    | dept_id 
------+-----------+---------
 Sita | Kathmandu |      10
 Ram  | Pokhara   |      10
 Hari | Kathmandu |      20
 Gita | Lalitpur  |      30
(4 rows)

 sid | cid | marks 
-----+-----+-------
   1 | C1  |    85
   1 | C2  |    72
   3 | C2  |    91
(3 rows)
```

Ram's 64 became 69 (still below 70), so the delete removed him from C1: the two statements interacted in the order they were run. Run `SELECT` first to preview what a `DELETE` will remove.

## 6.7 Views

A **view** is a stored query presented as a virtual table. Uses: hide columns or rows (security), simplify complex joins, give a stable interface when tables change (logical data independence, Unit 2).

```sql
CREATE VIEW student_results AS
SELECT s.sid, s.name, c.title, e.marks
FROM student s JOIN enrollment e ON s.sid = e.sid JOIN course c ON c.cid = e.cid;
SELECT * FROM student_results WHERE marks > 70 ORDER BY sid;
CREATE OR REPLACE VIEW student_results AS
SELECT s.sid, s.name, c.title, e.marks, CASE WHEN e.marks >= 80 THEN 'distinction' ELSE 'pass' END AS grade
FROM student s JOIN enrollment e ON s.sid = e.sid JOIN course c ON c.cid = e.cid;
SELECT name, title, grade FROM student_results ORDER BY sid, title;
DROP VIEW student_results;
```
```output
 sid | name | title | marks 
-----+------+-------+-------
   1 | Sita | DBMS  |    85
   1 | Sita | DSA   |    72
   3 | Hari | DSA   |    91
(3 rows)

 name | title |    grade    
------+-------+-------------
 Sita | DBMS  | distinction
 Sita | DSA   | pass
 Hari | DSA   | distinction
(3 rows)
```

`CREATE OR REPLACE VIEW` (Oracle and PostgreSQL; MySQL the same; SQL Server uses `ALTER VIEW`) changes a view's definition. A view with joins or aggregates is usually **read-only**; a simple single-table view can be updated through (`WITH CHECK OPTION` forces new rows to satisfy its `WHERE`). A **materialised view** stores its result physically and must be refreshed.

## 6.8 Seeing the ideas: how a query is really read

All results below were produced by a real PostgreSQL server on the sample database of Section 6.1 (departments BCA, BIT, BBS; students Sita, Ram, Hari, Gita; courses C1 DBMS, C2 DSA, C3 Web Technology; four enrolment rows). The same query text is read in a different order from the order in which it is written, and a few small figures make that order clear.

```photogrid label="6.1" cols="2" ratio="1.1" caption="From campus to query result. (a) The Tribhuvan University campus at Kirtipur, Kathmandu. A university keeps millions of rows of students, subjects and marks, and every result look-up is a SELECT with a join. (b) The view result_view stores one join query under a name; the user writes SELECT * FROM result_view and receives the joined rows with a computed grade column, without knowing which base tables are involved."
@ photo id="bca202/tu" cap="Tribhuvan University, Kirtipur"
fit 1.1
focus 0.5 0.45
call 0.5 0.12 0.50 0.40 "results, fees, records: rows"
@ svg cap="result_view (real output)"
f = Fig(300, 250)
f.text(150, 12, "SELECT * FROM result_view ORDER BY marks DESC", size=8.5, color=NAVY, bold=True)
hd = [("name", 55), ("title", 55), ("marks", 50), ("grade", 110)]
rows = [("Hari", "DSA", "91", "Distinction"), ("Sita", "DBMS", "85", "Distinction"), ("Sita", "DSA", "72", "First"), ("Ram", "DBMS", "64", "First")]
for j, (h, w) in enumerate(hd):
    xx = 10 + sum(c[1] for c in hd[:j])
    f.box(xx, 24, w, 24, h, fill=NAVY, stroke=NAVY, color="#ffffff", size=9.5, bold=True, r=0)
    for i, r in enumerate(rows):
        f.box(xx, 48 + i * 24, w, 24, r[j], fill=BLUE if i % 2 == 0 else SOFT, stroke=NAVY, size=9.5, r=0, bold=(j == 3))
f.box(10, 160, 270, 78, "The view is a stored query,\nnot a stored copy of the data.\nChange a mark in enrollment and\nthe view shows it at once.", fill=MINT, stroke=TEAL, size=9.5, bold=True)
```

```svgfig label="6.1" caption="The logical order in which SQL evaluates a query, shown with the query SELECT c.title, COUNT(e.sid) FROM course c LEFT JOIN enrollment e ON e.cid = c.cid GROUP BY c.title ORDER BY c.title. FROM and JOIN come first and build the working rows (4 enrolment rows plus the unmatched course C3 give 5 rows). WHERE filters rows, GROUP BY forms groups (3 groups), HAVING filters groups, SELECT computes the output columns, and ORDER BY sorts last. This is why a column alias defined in SELECT cannot be used in WHERE, and why aggregates cannot appear in WHERE."
f = Fig(580, 200)
steps = [("1 FROM / JOIN", "5 working rows\n(C3 kept by LEFT JOIN)", BLUE, NAVY), ("2 WHERE", "filter rows\n(none here)", SAND, AMBER), ("3 GROUP BY", "3 groups\nDBMS, DSA, Web", MINT, TEAL), ("4 HAVING", "filter groups\n(none here)", SAND, AMBER), ("5 SELECT", "title, COUNT\n= 2, 2, 0", BLUE, NAVY), ("6 ORDER BY", "sort the 3 rows\nby title", ROSE, RED)]
for i, (a, b, fl, st) in enumerate(steps):
    x = 4 + i * 96
    f.box(x, 14, 88, 24, a, fill=st, stroke=st, color="#ffffff", size=9, bold=True)
    f.box(x, 38, 88, 56, b, fill=fl, stroke=st, size=9, bold=False)
    if i < 5:
        f.arrow([(x + 88, 26), (x + 96, 26)], color=SLATE, sw=1.4)
f.box(10, 118, 560, 62, "Result: DBMS 2 | DSA 2 | Web Technology 0\nWHERE cannot use aggregates (use HAVING); HAVING cannot see rows, only groups.\nLEFT JOIN keeps course C3 with a count of 0 because COUNT(e.sid) ignores NULL.", fill=SOFT, stroke=SLATE, size=10, bold=True)
```

```svgfig label="6.2" caption="NULL and three-valued logic. A comparison with NULL is neither true nor false but unknown, and WHERE keeps only rows for which the condition is true. So WHERE dept_id <> 10 returns only Hari (20); Gita, whose dept_id is NULL, is silently dropped. Adding OR dept_id IS NULL brings her back. The same idea explains why COUNT(dept_id) is 3 while COUNT(*) is 4."
f = Fig(580, 230)
hd = [("name", 80), ("dept_id", 80), ("dept_id <> 10", 120), ("kept by WHERE?", 120)]
rows = [("Sita", "10", "FALSE", "no"), ("Ram", "10", "FALSE", "no"), ("Hari", "20", "TRUE", "yes"), ("Gita", "NULL", "UNKNOWN", "no")]
for j, (h, w) in enumerate(hd):
    xx = 6 + sum(c[1] for c in hd[:j])
    f.box(xx, 8, w, 24, h, fill=NAVY, stroke=NAVY, color="#ffffff", size=9.5, bold=True, r=0)
    for i, r in enumerate(rows):
        bad = (i == 3)
        f.box(xx, 32 + i * 24, w, 24, r[j], fill=ROSE if bad else (BLUE if i % 2 == 0 else SOFT), stroke=RED if bad else NAVY, size=9.5, r=0, bold=(j == 3))
f.box(440, 8, 130, 120, "COUNT(*) = 4\nCOUNT(dept_id) = 3\nCOUNT(DISTINCT\ncity) = 3\n\nAggregates ignore NULL", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(6, 150, 560, 70, "WHERE dept_id <> 10                       -> Hari\nWHERE dept_id <> 10 OR dept_id IS NULL  -> Hari, Gita\nTest for NULL only with IS NULL / IS NOT NULL, never with = NULL.", fill=SAND, stroke=AMBER, size=10, bold=True)
```

```svgfig label="6.3" caption="Two kinds of subquery with real results. In the uncorrelated query on the left the inner query SELECT AVG(marks) runs once and returns 78; the outer query then keeps the students whose marks exceed 78, namely Sita (85) and Hari (91). In the correlated query on the right the inner query refers to the outer row (e.sid = s.sid) and runs again for every student; NOT EXISTS keeps Gita, the only student with no enrolment."
f = Fig(580, 240)
f.text(145, 12, "Uncorrelated: inner runs once", size=10.5, color=TEAL, bold=True)
f.box(10, 24, 270, 40, "SELECT name FROM student WHERE sid IN (\n SELECT sid FROM enrollment WHERE marks >", fill=SOFT, stroke=SLATE, size=8.5)
f.box(10, 70, 270, 24, "(SELECT AVG(marks) FROM enrollment))", fill=MINT, stroke=TEAL, size=8.5, bold=True)
f.arrow([(145, 94), (145, 112)], color=SLATE, sw=1.5, label="AVG = 78", lpos=(200, 106), lsize=9)
f.box(30, 112, 230, 30, "marks > 78: sid 1 (85), sid 3 (91)", fill=BLUE, stroke=NAVY, size=9.5, bold=True)
f.arrow([(145, 142), (145, 160)], color=SLATE, sw=1.5)
f.box(60, 160, 170, 30, "Sita, Hari", fill=MINT, stroke=TEAL, size=11, bold=True)
f.text(435, 12, "Correlated: inner runs per row", size=10.5, color=RED, bold=True)
f.box(300, 24, 270, 64, "SELECT name FROM student s WHERE\nNOT EXISTS (SELECT 1 FROM enrollment e\n WHERE e.sid = s.sid)", fill=SOFT, stroke=SLATE, size=8.5)
rowsx = [("Sita", "has rows -> out"), ("Ram", "has rows -> out"), ("Hari", "has rows -> out"), ("Gita", "no rows -> KEPT")]
for i, (n, r) in enumerate(rowsx):
    f.box(300, 96 + i * 24, 70, 24, n, fill=BLUE, stroke=NAVY, size=9.5, r=0, bold=True)
    f.box(370, 96 + i * 24, 200, 24, r, fill=(ROSE if i == 3 else SOFT), stroke=NAVY, size=9.5, r=0, bold=(i == 3))
f.text(435, 206, "result: Gita", size=11, color=RED, bold=True)
f.text(290, 232, "IN and comparison subqueries usually run once; EXISTS tests are checked per outer row", size=9.5, color=SLATE, bold=True)
```

### 6.8.1 Eight benefits of views

1. **Simplicity for the user.** A view hides a long join behind a short name. A clerk writes `SELECT * FROM result_view` instead of joining three tables, and cannot make a join mistake. Complex logic is written once by an expert and reused by everyone.
2. **Security.** A view can show only some columns and rows, such as a student's name and marks without fee details. Users are given permission on the view and none on the base tables. A teller in a Nepali bank can therefore see balances and not loan files.
3. **Logical data independence.** If a base table is split or renamed, the view can be redefined to give the same columns. Programs that use the view keep working. This is the logical data independence of the three-level architecture in practice.
4. **Always current data.** A view stores its query, not a copy of the data. When a mark changes in enrollment, the next `SELECT` from result_view shows the new value at once. Reports based on views never go out of date.
5. **Consistent business rules.** A computed column such as the grade in result_view (80 or more is Distinction, 60 or more is First) is defined in one place. Every report that uses the view applies the same rule. This prevents two reports giving different grades to the same student.
6. **Different views for different people.** The exam office, the library and the principal can each have a view of the same tables in the layout they need. The tables are not copied or duplicated. Each group works with the shape of data that suits its work.
7. **Simpler reports and tools.** Reporting tools and spreadsheets can connect to a view as if it were a table. Developers do not need to understand the underlying design. Report writing becomes faster.
8. **Controlled updates.** A simple view on one table can be used to insert, update or delete rows, and `WITH CHECK OPTION` refuses changes that would make a row disappear from the view. Views with joins, groups or aggregates are generally read-only. This keeps updates predictable and safe.

## Formula and fact sheet

- Evaluation order: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
- `WHERE` filters rows; `HAVING` filters groups. `COUNT(*)` counts rows; `COUNT(col)` skips NULL.
- `= NULL` is never true; use `IS NULL`. Prefer `NOT EXISTS` to `NOT IN`.
- Joins: INNER, LEFT, RIGHT, FULL, CROSS. Set operators: UNION, INTERSECT, EXCEPT.
- `UPDATE`/`DELETE` without `WHERE` affect all rows.

## Chapter summary

- `SELECT` filters, sorts, groups and aggregates; joins combine tables; subqueries nest one query in another.
- NULL needs special handling in comparisons and `NOT IN`.
- `UPDATE` and `DELETE` change data and need careful `WHERE` clauses.
- Views give named, reusable, controlled windows onto the data.

## Practice

(Use the sample database of 6.1 in its original state.)

1. List names of students from Kathmandu.
2. Find the average marks per course, only for courses with an average above 75.
3. List students and their department names, including students with no department.
4. Find students who are enrolled in no course.
5. Find the student(s) with the highest mark in DSA (C2) using a subquery.
6. Raise all marks in C2 by 3 but not above 100.
7. Delete enrolments of students whose department is BIT.
8. Create a view `bca_students` of students in department 10.
9. Differentiate `WHERE` and `HAVING`; `UNION` and `UNION ALL`.

::: note Answers and worked solutions
**1.** `SELECT name FROM student WHERE city = 'Kathmandu';` → Sita, Hari.
**2.** `SELECT cid, avg(marks) FROM enrollment GROUP BY cid HAVING avg(marks) > 75;` → C2 (81.5); C1 has 74.5.
**3.** `SELECT s.name, d.dept_name FROM student s LEFT JOIN department d ON s.dept_id = d.dept_id;`
**4.** `SELECT name FROM student s WHERE NOT EXISTS (SELECT 1 FROM enrollment e WHERE e.sid = s.sid);` → Gita.
**5.** `SELECT sid FROM enrollment WHERE cid = 'C2' AND marks = (SELECT max(marks) FROM enrollment WHERE cid = 'C2');` → student 3 (91).
**6.** `UPDATE enrollment SET marks = LEAST(marks + 3, 100) WHERE cid = 'C2';` (Oracle/MySQL also have `LEAST`).
**7.** `DELETE FROM enrollment WHERE sid IN (SELECT sid FROM student WHERE dept_id = 20);` removes Hari's row.
**8.** `CREATE VIEW bca_students AS SELECT * FROM student WHERE dept_id = 10;`
**9.** `WHERE` filters rows before grouping, `HAVING` filters groups after aggregation. `UNION` removes duplicate rows, `UNION ALL` keeps them (and is faster).
:::

## Model answers (5 and 10 marks)

**Q1 (5 marks). What is a join? Explain inner join and left outer join with examples.**

*Introduction.* A join combines rows from two or more tables on a related column, usually a foreign key matched to a primary key. It rebuilds, at query time, the facts that normalisation spread over several tables.

1. **Inner join.** It returns only the rows that match in both tables. The query `SELECT s.name, c.title, e.marks FROM student s JOIN enrollment e ON e.sid = s.sid JOIN course c ON c.cid = e.cid WHERE e.marks >= 70 ORDER BY e.marks DESC;` returned Hari (DSA, 91), Sita (DBMS, 85) and Sita (DSA, 72). Ram's 64 was removed by WHERE.
2. **Left outer join.** It keeps every row of the left table and fills the right side with NULL when there is no match. `SELECT s.name, d.dept_name FROM student s LEFT JOIN department d ON d.dept_id = s.dept_id;` returned Sita BCA, Ram BCA, Hari BIT and Gita with an empty department, whereas the inner join would have dropped Gita.
3. **Right and full outer join.** The right outer join keeps every row of the right table, and the full outer join keeps unmatched rows from both sides.
4. **Cross join.** It pairs every row with every row: 4 students and 3 departments give 12 rows. It is rarely wanted by accident.
5. **Joining three tables.** Each extra table needs its own ON condition, as with student, enrollment and course above.

*Conclusion.* Use an inner join when only matching rows matter and an outer join when rows must not be lost, for example listing all students including those without a department.

**Q2 (5 marks). Differentiate WHERE and HAVING. Explain GROUP BY with an example.**

*Introduction.* GROUP BY collects rows with the same value in the chosen column into groups so that an aggregate function (COUNT, SUM, AVG, MIN, MAX) gives one result per group (Figure 6.1).

1. **GROUP BY.** `SELECT c.title, COUNT(e.sid) AS takers, AVG(e.marks) FROM course c LEFT JOIN enrollment e ON e.cid = c.cid GROUP BY c.title;` returned DBMS 2 and 74.5, DSA 2 and 81.5, and Web Technology 0 with a NULL average.
2. **WHERE.** It filters individual rows before grouping, and it cannot contain aggregate functions.
3. **HAVING.** It filters groups after grouping and can use aggregates. `SELECT city, COUNT(*) FROM student GROUP BY city HAVING COUNT(*) > 1;` returned only Kathmandu, with 2 students.
4. **Order of work.** FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.
5. **Rule.** Every column in SELECT must be either in GROUP BY or inside an aggregate function.
6. **NULL.** Aggregates ignore NULL: COUNT(dept_id) is 3 but COUNT(*) is 4.

| Point | WHERE | HAVING |
|---|---|---|
| Filters | rows | groups |
| Applied | before GROUP BY | after GROUP BY |
| Aggregates | not allowed | allowed |

*Conclusion.* WHERE reduces the rows that enter the groups, and HAVING reduces the groups that leave.

**Q3 (10 marks). What is a nested query (subquery)? Explain the types with examples, and describe views with their advantages.**

*Introduction.* A subquery is a SELECT statement written inside another statement, in the WHERE, FROM or SELECT part. It lets the answer of one question become the input of another, so a question such as "who scored above the average?" needs one statement and not two (Figure 6.3). A view stores such a query under a name.

*Types of subquery.*
1. **Scalar subquery** returns one value, for example `(SELECT AVG(marks) FROM enrollment)`, which is 78.
2. **Multi-row subquery** returns a column of values and is used with IN, ANY or ALL. The query `SELECT name FROM student WHERE sid IN (SELECT sid FROM enrollment WHERE marks > (SELECT AVG(marks) FROM enrollment));` returned Sita and Hari.
3. **Correlated subquery** refers to the outer row and runs for each row. `SELECT name FROM student s WHERE NOT EXISTS (SELECT 1 FROM enrollment e WHERE e.sid = s.sid);` returned Gita, who has no enrolment.
4. **Derived table** is a subquery in FROM that acts as a temporary table.
5. **EXISTS and NOT EXISTS** test only whether the inner query returns any row, and are usually safe with NULL values, unlike `NOT IN`.

*Views.* A view is a named SELECT stored in the database:

```sql
CREATE VIEW result_view AS
SELECT s.name, c.title, e.marks,
       CASE WHEN e.marks >= 80 THEN 'Distinction'
            WHEN e.marks >= 60 THEN 'First' ELSE 'Pass' END AS grade
FROM student s JOIN enrollment e ON e.sid = s.sid JOIN course c ON c.cid = e.cid;
```

Selecting from it returned four rows: Hari DSA 91 Distinction, Sita DBMS 85 Distinction, Sita DSA 72 First and Ram DBMS 64 First.

*Advantages of views.* Simplicity (a long join becomes one name), security (hide columns and rows), logical data independence, always-current data, one place for business rules, and different shapes of the same data for different users (Section 6.8.1).

| Point | Subquery | View |
|---|---|---|
| Lives | inside one statement | in the database, reusable |
| Stores data | no | no (stores the query) |
| Purpose | answer a step of a question | simplify and protect |

*Conclusion.* Subqueries let SQL express multi-step questions in one statement, and views package such queries so that users get simple, secure and always up-to-date access to the data.
