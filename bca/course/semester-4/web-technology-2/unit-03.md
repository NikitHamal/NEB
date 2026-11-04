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

## 3.7 Seeing the ideas: how MySQL stores, filters and joins data

A web application is only as good as the database behind it. The plate shows the man who wrote MySQL and the kind of disk hardware on which a database file really lives. The figures then run the Unit 3 queries on a real MariaDB 10.11.19 server, which speaks the same SQL as MySQL, and show the true row counts, the true numbers and the true error messages.

```photogrid label="3.1" cols="3" ratio="1.25" caption="From idea to storage. (a) Michael 'Monty' Widenius wrote the first MySQL in Finland in 1995 and later started MariaDB, the MySQL-compatible server used to check every query in this book. (b) The IBM 305 RAMAC disk unit of 1956, the first commercial hard disk, held about 5 million characters; a modern MySQL server still keeps its tables in files on a disk, only vastly larger and faster. (c) PHP, phpMyAdmin and the mysql command are all clients of the same server on port 3306."
@ photo id="bca255/monty" cap="Monty Widenius, author of MySQL"
fit 1.25
focus 0.5 0.5
@ photo id="bca202/ramac" cap="IBM RAMAC disk, 1956"
fit 1.25
focus 0.5 0.5
@ svg cap="Many clients, one server"
f = Fig(300, 250)
for i, n in enumerate(["PHP script", "phpMyAdmin", "mysql command"]):
    f.box(6, 10 + i * 50, 120, 38, n, fill=BLUE, stroke=NAVY, size=12.5, bold=True)
    f.arrow([(128, 29 + i * 50), (168, 85)], color=SLATE, sw=1.6)
f.box(170, 40, 124, 90, "", fill=MINT, stroke=TEAL)
f.text(232, 62, "mysqld", size=15, color=TEAL, bold=True)
f.text(232, 86, "port 3306", size=12.5, color=SLATE)
f.text(232, 108, "user + password", size=12.5, color=SLATE)
f.arrow([(232, 132), (232, 168)], color=TEAL, sw=1.8)
f.box(170, 170, 124, 40, "data files on disk", fill=SAND, stroke=AMBER, size=12.5, bold=True)
f.text(80, 190, "all share the", size=12.5, color=NAVY, bold=True)
f.text(80, 210, "same tables", size=12.5, color=NAVY, bold=True)
```

```svgfig label="3.1" caption="The order in which MySQL really runs a query, with real row counts from the student table of five rows. FROM reads all 5 rows; WHERE marks >= 60 keeps 4 (Bikash with 55 is removed before anything is grouped); GROUP BY dept makes 2 groups, BCA (84.75) and BIT (74.88); HAVING AVG(marks) > 80 keeps 1 group because a group condition cannot be tested before the groups exist; ORDER BY and LIMIT then shape the output. This is why WHERE cannot use COUNT or AVG and HAVING can."
f = Fig(580, 222)
steps = [("FROM", "student", "5 rows", BLUE, NAVY), ("WHERE", "marks >= 60", "4 rows", BLUE, NAVY), ("GROUP BY", "dept", "2 groups", SAND, AMBER), ("HAVING", "AVG(marks) > 80", "1 group", SAND, AMBER), ("ORDER BY", "+ LIMIT 5", "1 row", MINT, TEAL)]
for i, (a, b, c, fl, st) in enumerate(steps):
    x = 6 + i * 115
    f.box(x, 12, 104, 70, "", fill=fl, stroke=st)
    f.text(x + 52, 30, a, size=11.5, color=st, bold=True)
    f.text(x + 52, 48, b, size=9.5, color=SLATE)
    f.text(x + 52, 70, c, size=11.5, color=st, bold=True)
    if i < 4:
        f.arrow([(x + 106, 47), (x + 113, 47)], color=SLATE, sw=1.5)
f.text(8, 108, "real rows after WHERE marks >= 60", size=10.5, color=NAVY, bold=True, anchor="start")
data = [("Ram", "BCA", 78.50, True), ("Sita", "BCA", 91.00, True), ("Hari", "BIT", 64.25, True), ("Gita", "BIT", 85.50, True), ("Bikash", "BCA", 55.00, False)]
for i, (n, d, m, ok) in enumerate(data):
    y = 118 + i * 20
    f.box(8, y, 250, 17, "", fill=MINT if ok else ROSE, stroke=TEAL if ok else RED, r=3, sw=1)
    f.text(18, y + 9, "%s   %s   %.2f" % (n, d, m), size=10, color=SLATE, anchor="start", vmid=True)
    f.text(250, y + 9, "kept" if ok else "removed", size=9.5, color=TEAL if ok else RED, bold=True, anchor="end", vmid=True)
f.text(300, 128, "groups made", size=10.5, color=NAVY, bold=True, anchor="start")
f.box(300, 136, 130, 22, "BCA  n=2  avg 84.75", fill=SAND, stroke=AMBER, size=9.5, bold=True, r=3)
f.box(300, 162, 130, 22, "BIT  n=2  avg 74.88", fill=SAND, stroke=AMBER, size=9.5, bold=True, r=3)
f.arrow([(432, 147), (456, 147)], color=SLATE, sw=1.4)
f.text(462, 143, "avg > 80", size=9.5, color=TEAL, bold=True, anchor="start")
f.text(462, 156, "kept", size=9.5, color=TEAL, bold=True, anchor="start")
f.arrow([(432, 173), (456, 173)], color=RED, sw=1.4)
f.text(462, 177, "dropped", size=9.5, color=RED, bold=True, anchor="start")
f.text(300, 214, "result: BCA, 2, 84.75", size=11, color=TEAL, bold=True, anchor="start")
```

```svgfig label="3.2" caption="INNER JOIN against LEFT JOIN on the tables dept (BCA, BIT, BBA) and student (five students), real results. The inner join keeps only matching pairs, so 5 rows are returned and the department BBA, which has no students, disappears. The left join keeps every row of the left table, so BBA appears with NULL in the name column and the count is 6. A LEFT JOIN with a test for NULL on the right side is the standard way to find departments without students."
f = Fig(580, 214)
f.box(8, 8, 120, 56, "", fill=BLUE, stroke=NAVY)
f.text(68, 24, "dept", size=11.5, color=NAVY, bold=True)
f.text(68, 42, "BCA  BIT  BBA", size=10, color=SLATE)
f.box(152, 8, 120, 56, "", fill=BLUE, stroke=NAVY)
f.text(212, 24, "student", size=11.5, color=NAVY, bold=True)
f.text(212, 42, "5 rows: BCA 3, BIT 2", size=9.5, color=SLATE)
f.arrow([(130, 36), (150, 36)], color=SLATE, sw=1.4, both=True)
f.text(140, 80, "ON s.dept = d.code", size=9.5, color=SLATE, bold=False)
f.text(300, 24, "INNER JOIN  ->  5 rows", size=11.5, color=TEAL, bold=True, anchor="start")
f.text(300, 44, "BBA is missing", size=10.5, color=RED, bold=True, anchor="start")
f.text(300, 64, "LEFT JOIN  ->  6 rows", size=11.5, color=AMBER, bold=True, anchor="start")
f.text(300, 84, "BBA kept with NULL", size=10.5, color=AMBER, bold=True, anchor="start")
rows = [("BBA", "NULL"), ("BCA", "Ram"), ("BCA", "Sita"), ("BCA", "Bikash"), ("BIT", "Hari"), ("BIT", "Gita")]
f.box(8, 104, 90, 20, "code", fill=SOFT, stroke=NAVY, size=10, bold=True, r=2)
f.box(98, 104, 120, 20, "name", fill=SOFT, stroke=NAVY, size=10, bold=True, r=2)
for i, (c, n) in enumerate(rows):
    y = 124 + i * 14
    hl = c == "BBA"
    f.box(8, y, 90, 14, c, fill=SAND if hl else MINT, stroke=AMBER if hl else TEAL, size=9, r=0, sw=0.8)
    f.box(98, y, 120, 14, n, fill=SAND if hl else MINT, stroke=AMBER if hl else TEAL, size=9, r=0, sw=0.8)
f.text(240, 140, "real result of the LEFT JOIN", size=10, color=NAVY, bold=True, anchor="start")
f.text(240, 158, "the only row an inner join loses", size=10, color=AMBER, bold=True, anchor="start")
f.text(240, 176, "is the highlighted BBA row", size=10, color=AMBER, bold=True, anchor="start")
f.text(240, 200, "5 + 1 = 6 rows", size=11, color=TEAL, bold=True, anchor="start")
```

```svgfig label="3.3" caption="Why money is stored as DECIMAL and never as FLOAT. Ten rows of 0.10 were inserted into a FLOAT column and a DECIMAL(10,2) column and added up by MariaDB. The FLOAT total prints as 1.0000000149011612 and the test total = 1 is false (0), while the DECIMAL total is exactly 1.00 and the test is true (1). A fee system that adds thousands of such amounts with FLOAT would slowly drift away from the true total; DECIMAL does exact decimal arithmetic."
f = Fig(580, 168)
f.box(8, 10, 270, 120, "", fill=ROSE, stroke=RED)
f.text(143, 30, "FLOAT  (approximate)", size=12, color=RED, bold=True)
f.text(143, 56, "10 x 0.1 added gives", size=10.5, color=SLATE)
f.text(143, 80, "1.0000000149011612", size=13, color=RED, bold=True)
f.text(143, 104, "SUM(f) = 1   is   0  (false)", size=10.5, color=RED, bold=True)
f.box(302, 10, 270, 120, "", fill=MINT, stroke=TEAL)
f.text(437, 30, "DECIMAL(10,2)  (exact)", size=12, color=TEAL, bold=True)
f.text(437, 56, "10 x 0.10 added gives", size=10.5, color=SLATE)
f.text(437, 80, "1.00", size=15, color=TEAL, bold=True)
f.text(437, 104, "SUM(d) = 1   is   1  (true)", size=10.5, color=TEAL, bold=True)
f.text(290, 154, "use DECIMAL for fees, prices, salaries and balances", size=11, color=NAVY, bold=True)
```

```svgfig label="3.4" caption="Four constraints, four refusals, all real server messages. NOT NULL (error 1048) refuses a missing name, UNIQUE (error 1062) refuses a second e-mail ram@tu.edu.np, CHECK (error 4025 in MariaDB; MySQL 8 reports 3819) refuses marks of 150, and the FOREIGN KEY (error 1452) refuses a student in the department MBA that does not exist. The same key also protects the parent table: deleting department BCA while students refer to it is refused with error 1451. All five errors share SQLSTATE 23000, the class for integrity-constraint violations."
f = Fig(580, 212)
rows = [("NOT NULL", "1048", "Column 'name' cannot be null"), ("UNIQUE", "1062", "Duplicate entry 'ram@tu.edu.np' for key 'email'"), ("CHECK", "4025", "CONSTRAINT student.marks failed (marks = 150)"), ("FOREIGN KEY", "1452", "Cannot add a child row: department MBA is absent"), ("FOREIGN KEY", "1451", "Cannot delete a parent row: BCA still has students")]
f.text(60, 14, "constraint", size=10.5, color=NAVY, bold=True)
f.text(150, 14, "error", size=10.5, color=NAVY, bold=True)
f.text(215, 14, "message from the server", size=10.5, color=NAVY, bold=True, anchor="start")
for i, (c, e, m) in enumerate(rows):
    y = 24 + i * 34
    f.box(8, y, 104, 28, c, fill=BLUE, stroke=NAVY, size=10.5, bold=True, r=3)
    f.box(118, y, 66, 28, e, fill=ROSE, stroke=RED, size=12, bold=True, r=3)
    f.box(190, y, 382, 28, "", fill="#ffffff", stroke=SLATE, r=3, sw=1)
    f.text(198, y + 14, m, size=10, color=SLATE, anchor="start", vmid=True)
f.text(290, 206, "SQLSTATE 23000 for all: integrity constraint violation", size=10.5, color=TEAL, bold=True)
```

### 3.7.1 Eight advantages of MySQL for web applications

1. **It is free and open source.** The community edition of MySQL, and the compatible MariaDB, cost nothing to use. A small business in Biratnagar can run its billing system without a database licence. This keeps the cost of a new web project low.
2. **It is fast for common web workloads.** Most websites read data far more often than they write it, and MySQL is tuned for this. An index on a column such as `roll` finds a student without scanning the whole table. A result page for thousands of students therefore opens quickly.
3. **It works with PHP out of the box.** The `mysqli` and `PDO` extensions are included with almost every PHP installation. A few lines connect a script to the server (Unit 4). This is why PHP and MySQL are taught together.
4. **It is easy to learn and use.** SQL reads almost like English, so `SELECT name FROM student WHERE marks > 80` is understood at once. Free tools such as phpMyAdmin give a graphical view of tables. A beginner can create a working database in an afternoon.
5. **It enforces data integrity.** Primary keys, `UNIQUE`, `NOT NULL`, `CHECK` and foreign keys refuse wrong data before it is stored (Fig. 3.4). A fee table cannot hold a payment for a student who does not exist. The database therefore protects the data even if the PHP code has a bug.
6. **It supports transactions and many users.** The InnoDB engine keeps a table consistent when several visitors write at once, and a transaction can group several changes into one all-or-nothing step. An online ticket booking can take money and reserve the seat together. If one step fails, both are cancelled.
7. **It scales and is available everywhere.** MySQL runs on Linux, Windows and macOS, from a laptop to a large server cluster, and cloud providers offer it as a managed service. A site can start small and grow. Moving to a bigger machine does not require rewriting the queries.
8. **It has a large community and good tools.** Backups with `mysqldump`, replication, users and privileges, and plenty of tutorials are available. Most hosting companies in Nepal offer MySQL with every plan. When something goes wrong, an answer is usually easy to find.

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

## Model answers (5 and 10 marks)

**Q1. What is MySQL? Explain its main data types and write SQL to create a table with constraints. Show how the constraints protect the data. (10 marks)**

**Introduction.** MySQL is an open-source relational database server. It stores data in tables of rows and columns and is used by programs through the language SQL. A client such as a PHP script, phpMyAdmin or the `mysql` command connects to the server on port 3306 with a user name and password (Plate 3.1). MariaDB is a compatible fork, and every query in this unit was run on it.

**Main data types.**

| Group | Types | Use |
|---|---|---|
| Integer | `TINYINT`, `INT`, `BIGINT` | counts, identifiers; `AUTO_INCREMENT` for keys |
| Exact decimal | `DECIMAL(p,s)` | money, marks with fixed decimals |
| Approximate | `FLOAT`, `DOUBLE` | measurements, never money |
| Text | `CHAR`, `VARCHAR(n)`, `TEXT` | names, e-mail, long text (use `utf8mb4`) |
| Date and time | `DATE`, `TIME`, `DATETIME`, `TIMESTAMP` | birthdays, orders |
| Other | `ENUM`, `BOOLEAN`, `JSON`, `BLOB` | fixed choices, flags, documents |

**Constraints.**

1. `PRIMARY KEY` identifies each row uniquely and is never null.
2. `NOT NULL` forces a value to be given.
3. `UNIQUE` refuses a repeated value (for example an e-mail).
4. `DEFAULT` supplies a value when none is given.
5. `CHECK (condition)` refuses values outside a rule, such as marks above 100.
6. `FOREIGN KEY ... REFERENCES` keeps a child row linked to an existing parent row.

```sql
CREATE TABLE dept (code VARCHAR(10) PRIMARY KEY, head VARCHAR(40));
CREATE TABLE student (
    roll  INT AUTO_INCREMENT PRIMARY KEY,
    name  VARCHAR(50) NOT NULL,
    dept  VARCHAR(10) NOT NULL DEFAULT 'BCA',
    marks DECIMAL(5,2) CHECK (marks BETWEEN 0 AND 100),
    email VARCHAR(80) UNIQUE,
    FOREIGN KEY (dept) REFERENCES dept(code)
) DEFAULT CHARSET = utf8mb4;
INSERT INTO dept VALUES ('BCA','Dr. Shah'),('BIT','Dr. Rai');
INSERT INTO student (name, dept, marks, email) VALUES ('Ram','BCA',78.50,'ram@tu.edu.np');
SELECT roll, name, dept, marks FROM student;
```
```output
+------+------+------+-------+
| roll | name | dept | marks |
+------+------+------+-------+
|    1 | Ram  | BCA  | 78.50 |
+------+------+------+-------+
```

**Protection in action (Fig. 3.4).** A second student with the e-mail `ram@tu.edu.np` is refused with error 1062; marks of 150 are refused by `CHECK` (error 4025 in MariaDB); a student in the department `MBA` is refused with error 1452 because no such parent row exists.

**Conclusion.** MySQL gives a web application a safe, shared store. Choosing the right type for each column and declaring constraints in the table definition let the database itself refuse wrong data, so the integrity of the records does not depend on every PHP script being correct. For a college this means that a mark list, a fee table and a library register stay consistent even when several teachers and clerks use the web pages at the same time.

**Q2. Differentiate between WHERE and HAVING. Explain with a GROUP BY example. (5 marks)**

Both clauses filter, but at different stages of a query (Fig. 3.1).

1. **WHERE** filters individual **rows** before grouping. It cannot use aggregate functions such as `COUNT` or `AVG`, because the groups do not exist yet.
2. **HAVING** filters **groups** after `GROUP BY`. It can use aggregate functions.
3. **Order of execution:** `FROM`, then `WHERE`, `GROUP BY`, `HAVING`, `SELECT`, `ORDER BY`, `LIMIT`.
4. **Speed:** a condition on a plain column is better placed in `WHERE`, since it removes rows early and the grouping has less work.
5. **Together:** the same query can use both, as in the example below.

In the example the students with marks of 60 or more are kept by `WHERE`, they are grouped by department, and `HAVING` keeps only the departments whose average is above 80.

```sql
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), dept VARCHAR(10), marks DECIMAL(5,2));
INSERT INTO student VALUES (1,'Ram','BCA',78.5),(2,'Sita','BCA',91),(3,'Hari','BIT',64.25),(4,'Gita','BIT',85.5),(5,'Bikash','BCA',55);
SELECT dept, COUNT(*) AS n, ROUND(AVG(marks), 2) AS avg_marks
FROM student WHERE marks >= 60
GROUP BY dept HAVING AVG(marks) > 80;
```
```output
+------+---+-----------+
| dept | n | avg_marks |
+------+---+-----------+
| BCA  | 2 |     84.75 |
+------+---+-----------+
```

Real result: five rows enter, four pass `WHERE`, two groups are made (BCA 84.75 and BIT 74.88), and only BCA passes `HAVING`. Bikash with 55 never reached the grouping, and this is exactly why a condition on a plain column is cheaper in `WHERE` than in `HAVING`.

**Q3. What is a join? Explain INNER JOIN and LEFT JOIN with SQL examples, and mention the other kinds. (10 marks)**

**Introduction.** Data in a relational database is split into several tables to avoid repetition: students in one table and departments in another, linked by a foreign key. A **join** combines the rows of two tables on a condition, normally *foreign key = primary key*, so that a query can show a student's name together with the head of the department.

**Kinds of join.**

1. **INNER JOIN** returns only pairs of rows that match the condition. Rows without a partner are dropped.
2. **LEFT JOIN** returns every row of the left table and the matching rows of the right table; where there is no match, the right columns are `NULL`.
3. **RIGHT JOIN** is the mirror of the left join and keeps all rows of the right table.
4. **FULL OUTER JOIN** keeps unmatched rows of both sides; MySQL has no direct form and uses `UNION` of a left and a right join.
5. **CROSS JOIN** pairs every row with every row (the Cartesian product); it is rarely wanted and grows quickly.
6. **Self join** joins a table to itself, for example an employee with their manager.

```sql
CREATE TABLE dept (code VARCHAR(10) PRIMARY KEY, head VARCHAR(40));
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), dept VARCHAR(10));
INSERT INTO dept VALUES ('BCA','Dr. Shah'),('BIT','Dr. Rai'),('BBA','Dr. Thapa');
INSERT INTO student VALUES (1,'Ram','BCA'),(2,'Sita','BCA'),(3,'Hari','BIT'),(4,'Gita','BIT'),(5,'Bikash','BCA');
SELECT s.name, d.head FROM student s INNER JOIN dept d ON s.dept = d.code ORDER BY s.roll;
SELECT d.code, COUNT(s.roll) AS students FROM dept d LEFT JOIN student s ON s.dept = d.code GROUP BY d.code ORDER BY d.code;
SELECT d.code FROM dept d LEFT JOIN student s ON s.dept = d.code WHERE s.roll IS NULL;
```
```output
+--------+----------+
| name   | head     |
+--------+----------+
| Ram    | Dr. Shah |
| Sita   | Dr. Shah |
| Hari   | Dr. Rai  |
| Gita   | Dr. Rai  |
| Bikash | Dr. Shah |
+--------+----------+
+------+----------+
| code | students |
+------+----------+
| BBA  |        0 |
| BCA  |        3 |
| BIT  |        2 |
+------+----------+
+------+
| code |
+------+
| BBA  |
+------+
```

**Reading the result (Fig. 3.2).** The inner join gives five rows and no BBA. The left join with `COUNT(s.roll)` keeps BBA with a count of 0, because `COUNT` of a column ignores `NULL`. The last query finds the departments with no students by keeping the rows where the right side is `NULL`.

| Point | INNER JOIN | LEFT JOIN |
|---|---|---|
| Unmatched left rows | dropped | kept with `NULL` |
| Result size | at most the matches | at least the left table |
| Typical question | which students have a department head | which departments have no students |

**Conclusion.** Joins let a database keep data in small, clean tables and still answer questions that need several of them. Use `INNER JOIN` when only matches matter and `LEFT JOIN` when every row of the main table must appear.

**Q4. Explain the aggregate functions of MySQL with a GROUP BY query. (5 marks)**

An **aggregate function** takes many rows and returns one value. They are normally used with `GROUP BY`, which makes one group per distinct value of a column.

1. `COUNT(*)` counts rows; `COUNT(col)` counts rows where `col` is not `NULL`.
2. `SUM(col)` adds the values; `AVG(col)` gives the mean.
3. `MIN(col)` and `MAX(col)` give the smallest and the largest value.
4. `GROUP BY dept` makes one result row for each department; every column in `SELECT` must be either grouped or aggregated.
5. `NULL` values are ignored by `SUM`, `AVG`, `MIN`, `MAX` and `COUNT(col)`.

```sql
CREATE TABLE student (roll INT PRIMARY KEY, name VARCHAR(50), dept VARCHAR(10), marks DECIMAL(5,2), email VARCHAR(80));
INSERT INTO student VALUES (1,'Ram','BCA',78.5,'ram@tu.edu.np'),(2,'Sita','BCA',91,'sita@tu.edu.np'),(3,'Hari','BIT',64.25,NULL),(4,'Gita','BIT',85.5,'gita@tu.edu.np'),(5,'Bikash','BCA',55,'bikash@tu.edu.np');
SELECT dept, COUNT(*) AS n, COUNT(email) AS with_email, MAX(marks) AS best, ROUND(AVG(marks),2) AS average
FROM student GROUP BY dept ORDER BY dept;
```
```output
+------+---+------------+-------+---------+
| dept | n | with_email | best  | average |
+------+---+------------+-------+---------+
| BCA  | 3 |          3 | 91.00 |   74.83 |
| BIT  | 2 |          1 | 85.50 |   74.88 |
+------+---+------------+-------+---------+
```

Note that BIT has two students but `COUNT(email)` gives 1, because Hari has no e-mail and `NULL` is skipped; this difference between `COUNT(*)` and `COUNT(col)` is a favourite examination trap. The average of BCA is 74.83 and the best mark is 91.00. In a PHP report page the same query would be run once, and the rows would be printed in an HTML table, so that the teacher sees the summary of every department without writing any loop over the students. Aggregates are also the basis of dashboards such as the number of admissions per programme.

**Q5. Why must DECIMAL be used for money in MySQL? What happens with FLOAT? (5 marks)**

`FLOAT` and `DOUBLE` store numbers in binary with a limited number of bits, so many decimal fractions, such as 0.1, cannot be stored exactly. `DECIMAL(p,s)` stores digits exactly, as decimal numbers.

1. **The test.** Ten rows of 0.1 were added in a `FLOAT` column and in a `DECIMAL(10,2)` column (Fig. 3.3).
2. **FLOAT result.** The total is 1.0000000149011612 and `SUM = 1` is false.
3. **DECIMAL result.** The total is exactly 1.00 and `SUM = 1` is true.
4. **Why it matters.** A fee or payroll system adds thousands of amounts; tiny errors add up, and a report that is one paisa out is rejected by an auditor.
5. **Rules.** Use `DECIMAL(10,2)` for rupees and paisa, keep the scale fixed, and in PHP pass money as strings or integers of paisa and not as `float`.

```sql
CREATE TABLE m (id INT AUTO_INCREMENT PRIMARY KEY, f FLOAT, d DECIMAL(10,2));
INSERT INTO m (f, d) VALUES (0.1,0.10),(0.1,0.10),(0.1,0.10),(0.1,0.10),(0.1,0.10),(0.1,0.10),(0.1,0.10),(0.1,0.10),(0.1,0.10),(0.1,0.10);
SELECT SUM(f) AS float_sum, SUM(d) AS decimal_sum, SUM(f) = 1 AS float_is_1, SUM(d) = 1 AS decimal_is_1 FROM m;
```
```output
+--------------------+-------------+------------+--------------+
| float_sum          | decimal_sum | float_is_1 | decimal_is_1 |
+--------------------+-------------+------------+--------------+
| 1.0000000149011612 |        1.00 |          0 |            1 |
+--------------------+-------------+------------+--------------+
```

The rule is simple: if a number is a quantity of rupees, it is a `DECIMAL`. A wallet or fee system that stores a balance as a float may show 99.99999999 instead of 100 after many operations, and a customer will notice it at once.
