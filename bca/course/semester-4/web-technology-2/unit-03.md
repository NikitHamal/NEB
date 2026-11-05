---
subject: Web Technology II
grade: BCA Semester 4
unit: 3
title: MySQL for Web Applications
hours: 7
area: BCA 255 · Web Technology II · Unit 3
---

A website without a database is a brochure. **MySQL** is the most widely used open-source relational database on the web; it stores the users, products, posts and results behind PHP pages. The theory of relations and SQL was the subject of Semester III's DBMS book; this unit is the working subset a web developer uses every day.

::: key What this unit gives you
- MySQL and its data types; creating databases and tables.
- `INSERT`, `SELECT`, `WHERE`, `UPDATE`, `DELETE`; aggregate functions, `ORDER BY`, `GROUP BY`; subqueries and joins.
- Constraints, and the real error messages you will meet.
:::

**Which server ran these examples.** Every SQL block below was executed on **MariaDB 10.11**, a drop-in, MySQL-compatible server (it is what `mysql` means on Debian and Ubuntu); the output tables are what the `mysql` client printed. MariaDB and Oracle MySQL 8 agree on everything used in this unit except that some error-message wording and `EXPLAIN` output differ slightly.

## 3.1 MySQL basics and data types

MySQL is a **client-server** database: the server (`mysqld`) owns the data; clients (the `mysql` command, phpMyAdmin, your PHP script) connect over a socket or TCP port 3306 with a user name and password. Commands end with `;`. A server hosts several **databases**, each with **tables**.

| Category | Types | Notes |
|---|---|---|
| Integer | `TINYINT`, `INT` (4 bytes), `BIGINT`, `UNSIGNED` | `AUTO_INCREMENT` for surrogate keys |
| Exact decimal | `DECIMAL(10,2)` | **use for money**, never `FLOAT` |
| Floating | `FLOAT`, `DOUBLE` | approximate |
| Text | `CHAR(n)`, `VARCHAR(n)`, `TEXT` | choose `utf8mb4` for Nepali and emoji |
| Date and time | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` | `'2026-11-02'` format |
| Other | `ENUM('a','b')`, `BOOLEAN` (= `TINYINT(1)`), `JSON`, `BLOB` | |

```sql
CREATE TABLE student (
    roll   INT AUTO_INCREMENT PRIMARY KEY,
    name   VARCHAR(50) NOT NULL,
    dept   VARCHAR(10) NOT NULL DEFAULT 'BCA',
    marks  DECIMAL(5,2) CHECK (marks BETWEEN 0 AND 100),
    email  VARCHAR(80) UNIQUE
) DEFAULT CHARSET = utf8mb4;
INSERT INTO student (name, dept, marks, email) VALUES
    ('Ram',    'BCA', 78.50, 'ram@tu.edu.np'),
    ('Sita',   'BCA', 91.00, 'sita@tu.edu.np'),
    ('Hari',   'BIT', 64.25, NULL),
    ('Gita',   'BIT', 85.50, 'gita@tu.edu.np'),
    ('Bikash', 'BCA', 55.00, 'bikash@tu.edu.np');
SHOW TABLES;
DESCRIBE student;
SELECT * FROM student;
```
```output
+----------------+
| Tables_in_demo |
+----------------+
| student        |
+----------------+
+-------+--------------+------+-----+---------+----------------+
| Field | Type         | Null | Key | Default | Extra          |
+-------+--------------+------+-----+---------+----------------+
| roll  | int(11)      | NO   | PRI | NULL    | auto_increment |
| name  | varchar(50)  | NO   |     | NULL    |                |
| dept  | varchar(10)  | NO   |     | BCA     |                |
| marks | decimal(5,2) | YES  |     | NULL    |                |
| email | varchar(80)  | YES  | UNI | NULL    |                |
+-------+--------------+------+-----+---------+----------------+
+------+--------+------+-------+------------------+
| roll | name   | dept | marks | email            |
+------+--------+------+-------+------------------+
|    1 | Ram    | BCA  | 78.50 | ram@tu.edu.np    |
|    2 | Sita   | BCA  | 91.00 | sita@tu.edu.np   |
|    3 | Hari   | BIT  | 64.25 | NULL             |
|    4 | Gita   | BIT  | 85.50 | gita@tu.edu.np   |
|    5 | Bikash | BCA  | 55.00 | bikash@tu.edu.np |
+------+--------+------+-------+------------------+
```
## 3.2 Querying: SELECT, WHERE, ORDER BY

```sql
CREATE TABLE student (roll INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), dept VARCHAR(10), marks DECIMAL(5,2));
INSERT INTO student (name, dept, marks) VALUES ('Ram','BCA',78.50),('Sita','BCA',91.00),('Hari','BIT',64.25),('Gita','BIT',85.50),('Bikash','BCA',55.00);
SELECT name, marks FROM student WHERE marks >= 70 ORDER BY marks DESC;
SELECT name FROM student WHERE dept = 'BCA' AND marks BETWEEN 50 AND 80;
SELECT name FROM student WHERE name LIKE '%a' OR dept IN ('BIT');
SELECT name, marks FROM student ORDER BY marks DESC LIMIT 2;
SELECT name, marks + 5 AS grace_marks, UPPER(dept) AS d FROM student WHERE roll <= 2;
```
```output
+------+-------+
| name | marks |
+------+-------+
| Sita | 91.00 |
| Gita | 85.50 |
| Ram  | 78.50 |
+------+-------+
+--------+
| name   |
+--------+
| Ram    |
| Bikash |
+--------+
+------+
| name |
+------+
| Sita |
| Hari |
| Gita |
+------+
+------+-------+
| name | marks |
+------+-------+
| Sita | 91.00 |
| Gita | 85.50 |
+------+-------+
+------+-------------+------+
| name | grace_marks | d    |
+------+-------------+------+
| Ram  |       83.50 | BCA  |
| Sita |       96.00 | BCA  |
+------+-------------+------+
```
`WHERE` filters rows: comparison (`= <> < >`), `AND OR NOT`, `BETWEEN`, `IN (…)`, `LIKE` (`%` any characters, `_` one), `IS NULL` (never `= NULL`). `ORDER BY col [ASC|DESC]`, `LIMIT n [OFFSET m]` (pagination), `DISTINCT` removes duplicates, `AS` renames.

## 3.3 Updating and deleting

```sql
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50) NOT NULL, marks DECIMAL(5,2), email VARCHAR(80) UNIQUE);
INSERT INTO student VALUES (1,'Ram',78.5,'ram@tu.edu.np'),(2,'Sita',91,'sita@tu.edu.np'),(3,'Hari',64.25,NULL);
UPDATE student SET marks = marks + 5 WHERE roll = 3;
SELECT roll, name, marks FROM student;
DELETE FROM student WHERE marks < 70;
SELECT COUNT(*) AS remaining FROM student;
```
```output
+------+------+-------+
| roll | name | marks |
+------+------+-------+
|    1 | Ram  | 78.50 |
|    2 | Sita | 91.00 |
|    3 | Hari | 69.25 |
+------+------+-------+
+-----------+
| remaining |
+-----------+
|         2 |
+-----------+
```
::: caution Always use a WHERE clause
`UPDATE student SET marks = 0;` or `DELETE FROM student;` without `WHERE` changes or deletes **every row**. Run the `SELECT` with the same `WHERE` first, and consider a transaction.
:::

**Constraints** protect integrity; the server refuses a bad change with a precise error (real messages from MariaDB):

```sql
-- raises
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50) NOT NULL, marks DECIMAL(5,2) CHECK (marks BETWEEN 0 AND 100), email VARCHAR(80) UNIQUE);
INSERT INTO student VALUES (1,'Ram',78.5,'ram@tu.edu.np');
INSERT INTO student VALUES (2,'Sita',91,'ram@tu.edu.np');
```
```output
--------------
INSERT INTO student VALUES (2,'Sita',91,'ram@tu.edu.np')
--------------

ERROR 1062 (23000) at line 4 in file: 'p.sql': Duplicate entry 'ram@tu.edu.np' for key 'email'
```
```sql
-- raises
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50) NOT NULL, marks DECIMAL(5,2) CHECK (marks BETWEEN 0 AND 100));
INSERT INTO student VALUES (1,'Ram',178);
```
```output
--------------
INSERT INTO student VALUES (1,'Ram',178)
--------------

ERROR 4025 (23000) at line 3 in file: 'p.sql': CONSTRAINT `student.marks` failed for `demo`.`student`
```
```sql
-- raises
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50) NOT NULL);
INSERT INTO student (roll) VALUES (1);
```
```output
--------------
INSERT INTO student (roll) VALUES (1)
--------------

ERROR 1364 (HY000) at line 3 in file: 'p.sql': Field 'name' doesn't have a default value
```
## 3.4 Aggregate functions, GROUP BY and HAVING

```sql
CREATE TABLE student (roll INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50), dept VARCHAR(10), marks DECIMAL(5,2));
INSERT INTO student (name, dept, marks) VALUES ('Ram','BCA',78.50),('Sita','BCA',91.00),('Hari','BIT',64.25),('Gita','BIT',85.50),('Bikash','BCA',55.00);
SELECT COUNT(*) AS n, SUM(marks) AS total, AVG(marks) AS mean, MIN(marks) AS lo, MAX(marks) AS hi FROM student;
SELECT dept, COUNT(*) AS n, ROUND(AVG(marks), 2) AS mean FROM student GROUP BY dept ORDER BY mean DESC;
SELECT dept, MAX(marks) AS best FROM student GROUP BY dept HAVING MAX(marks) > 90;
```
```output
+---+--------+-----------+-------+-------+
| n | total  | mean      | lo    | hi    |
+---+--------+-----------+-------+-------+
| 5 | 374.25 | 74.850000 | 55.00 | 91.00 |
+---+--------+-----------+-------+-------+
+------+---+-------+
| dept | n | mean  |
+------+---+-------+
| BIT  | 2 | 74.88 |
| BCA  | 3 | 74.83 |
+------+---+-------+
+------+-------+
| dept | best  |
+------+-------+
| BCA  | 91.00 |
+------+-------+
```
`COUNT(*)`, `SUM`, `AVG`, `MIN`, `MAX` collapse rows into one value (ignoring `NULL`, except `COUNT(*)`). `GROUP BY` makes one group per distinct value of the column(s); **`WHERE` filters rows before grouping, `HAVING` filters groups after it**.

## 3.5 Subqueries and joins

A **subquery** is a query inside another. A **join** combines rows of two tables on a condition, normally *foreign key = primary key*.

```sql
CREATE TABLE dept (code VARCHAR(10) PRIMARY KEY, head VARCHAR(40));
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), dept VARCHAR(10), marks DECIMAL(5,2),
                      FOREIGN KEY (dept) REFERENCES dept(code));
INSERT INTO dept VALUES ('BCA','Dr. Shah'),('BIT','Dr. Rai'),('BBA','Dr. Thapa');
INSERT INTO student VALUES (1,'Ram','BCA',78.5),(2,'Sita','BCA',91),(3,'Hari','BIT',64.25),(4,'Gita','BIT',85.5);
SELECT name, marks FROM student WHERE marks > (SELECT AVG(marks) FROM student);
SELECT s.name, d.head FROM student s INNER JOIN dept d ON s.dept = d.code ORDER BY s.roll;
SELECT d.code, COUNT(s.roll) AS students FROM dept d LEFT JOIN student s ON s.dept = d.code GROUP BY d.code;
SELECT name FROM student WHERE dept IN (SELECT code FROM dept WHERE head LIKE '%Rai');
```
```output
+------+-------+
| name | marks |
+------+-------+
| Sita | 91.00 |
| Gita | 85.50 |
+------+-------+
+------+----------+
| name | head     |
+------+----------+
| Ram  | Dr. Shah |
| Sita | Dr. Shah |
| Hari | Dr. Rai  |
| Gita | Dr. Rai  |
+------+----------+
+------+----------+
| code | students |
+------+----------+
| BBA  |        0 |
| BCA  |        2 |
| BIT  |        2 |
+------+----------+
+------+
| name |
+------+
| Hari |
| Gita |
+------+
```
`INNER JOIN` keeps only matching pairs; **`LEFT JOIN`** keeps every row of the left table, filling `NULL` where nothing matches (BBA has no students but still appears with 0). `IN (subquery)`, `EXISTS`, and scalar subqueries (a single value) cover most nested needs. The foreign key also stops you inserting a student of a department that does not exist:

```sql
-- raises
CREATE TABLE dept (code VARCHAR(10) PRIMARY KEY);
CREATE TABLE student (roll INT PRIMARY KEY, dept VARCHAR(10), FOREIGN KEY (dept) REFERENCES dept(code));
INSERT INTO dept VALUES ('BCA');
INSERT INTO student VALUES (1, 'MBA');
```
```output
--------------
INSERT INTO student VALUES (1, 'MBA')
--------------

ERROR 1452 (23000) at line 5 in file: 'p.sql': Cannot add or update a child row: a foreign key constraint fails (`demo`.`student`, CONSTRAINT `student_ibfk_1` FOREIGN KEY (`dept`) REFERENCES `dept` (`code`))
```
## 3.6 Administration notes

- **Users and privileges:** never connect the website as `root`; create a user with only the rights needed (`CREATE USER 'web'@'localhost' IDENTIFIED BY '…'; GRANT SELECT, INSERT, UPDATE, DELETE ON shop.* TO 'web'@'localhost';`).
- **Indexes** speed up `WHERE` and `JOIN` on a column (`CREATE INDEX idx_dept ON student(dept);`); primary keys and `UNIQUE` columns have them already.
- **Backup:** `mysqldump -u root -p dbname > backup.sql`; restore with `mysql -u root -p dbname < backup.sql`.
- **Engine:** use InnoDB (the default) for transactions and foreign keys.
- **phpMyAdmin** is a web interface for all of the above, bundled in XAMPP.

## Formula and fact sheet

- `CREATE TABLE` with `PRIMARY KEY`, `AUTO_INCREMENT`, `NOT NULL`, `UNIQUE`, `DEFAULT`, `CHECK`, `FOREIGN KEY`.
- `SELECT cols FROM t WHERE … GROUP BY … HAVING … ORDER BY … LIMIT n`.
- Aggregates: `COUNT SUM AVG MIN MAX`. `WHERE` before grouping, `HAVING` after.
- `INNER JOIN` (matches only), `LEFT JOIN` (all of the left table). `IS NULL`, never `= NULL`.
- `UPDATE`/`DELETE` always with `WHERE`. Money in `DECIMAL`.

## Chapter summary

- MySQL stores web data in tables; types, keys and constraints describe and protect it.
- A handful of statements (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) with `WHERE`, grouping, subqueries and joins covers most web needs.
- The server enforces constraints with clear errors, so design them into the schema.

## Practice

1. Create a table `book(id, title, price, stock)` with suitable types and constraints; insert four rows.
2. Write queries: books above NPR 500; the three most expensive; the average price.
3. Explain `WHERE` versus `HAVING` with an example.
4. Differentiate `INNER JOIN` and `LEFT JOIN`.
5. What happens on `INSERT` of a duplicate value into a `UNIQUE` column? Quote the error type.
6. Why must `DECIMAL` be used for money?
7. Write a query listing each department with the number of students, including departments with none.

::: note Answers and worked solutions
**1 and 2.**

```sql
CREATE TABLE book (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(80) NOT NULL, price DECIMAL(8,2) NOT NULL CHECK (price >= 0), stock INT NOT NULL DEFAULT 0);
INSERT INTO book (title, price, stock) VALUES ('C Programming', 450, 10), ('Java', 650, 4), ('Python', 700, 8), ('DBMS', 550, 0);
SELECT title FROM book WHERE price > 500;
SELECT title, price FROM book ORDER BY price DESC LIMIT 3;
SELECT AVG(price) AS average_price FROM book;
```
```output
+--------+
| title  |
+--------+
| Java   |
| Python |
| DBMS   |
+--------+
+--------+--------+
| title  | price  |
+--------+--------+
| Python | 700.00 |
| Java   | 650.00 |
| DBMS   | 550.00 |
+--------+--------+
+---------------+
| average_price |
+---------------+
|    587.500000 |
+---------------+
```
**3.** `WHERE` filters individual rows before grouping; `HAVING` filters whole groups after aggregation. Example: `SELECT dept, AVG(marks) FROM student WHERE marks > 40 GROUP BY dept HAVING AVG(marks) > 60;`
**4.** `INNER JOIN` returns only rows with a match in both tables. `LEFT JOIN` returns every row of the left table, with `NULL`s where the right table has no match (Section 3.5, BBA).
**5.** The server rejects it with error 1062, `Duplicate entry '…' for key '…'` (SQLSTATE 23000), as in the first constraint example of Section 3.3.
**6.** `FLOAT` stores binary approximations (0.1 cannot be exact), so sums drift by tiny amounts; `DECIMAL` stores exact decimal digits and is required for money.
**7.** `SELECT d.code, COUNT(s.roll) FROM dept d LEFT JOIN student s ON s.dept = d.code GROUP BY d.code;`
:::
