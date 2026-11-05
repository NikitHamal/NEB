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
