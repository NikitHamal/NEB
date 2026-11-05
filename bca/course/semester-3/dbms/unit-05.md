---
subject: Database Management System
grade: BCA Semester 3
unit: 5
title: Creating and Altering Database and Tables (SQL)
hours: 6
area: BCA 202 · Database Management System · Unit 5
---

**SQL** (Structured Query Language) is the standard language of relational databases. This unit covers the **DDL** part: creating databases and tables with constraints, altering them, and dropping them.

::: key What this unit gives you
- SQL basics, data types and dialect differences (Oracle, MySQL, PostgreSQL, SQL Server).
- `CREATE DATABASE`, `CREATE TABLE` with key, check and default constraints.
- `ALTER TABLE` to add or drop attributes and constraints; `DROP`, `TRUNCATE`.
- Every example below was executed on PostgreSQL; the output shown is real, including the error messages.
:::

## 5.1 Introduction to SQL

SQL was developed at IBM in the 1970s (as SEQUEL), standardised by ANSI/ISO from 1986 and is **declarative**: you state *what* you want. It is not case-sensitive for keywords; statements end with `;`; text literals use single quotes; `--` starts a comment. The lab syllabus uses Oracle, so the dialect table lists the differences you will meet.

| Feature | PostgreSQL | MySQL | Oracle | SQL Server |
|---|---|---|---|---|
| Text | `VARCHAR(n)`, `TEXT` | `VARCHAR(n)` | `VARCHAR2(n)` | `VARCHAR(n)`, `NVARCHAR` |
| Integer | `INT`, `BIGINT` | `INT` | `NUMBER(10)` | `INT` |
| Auto number | `SERIAL`, `GENERATED … AS IDENTITY` | `AUTO_INCREMENT` | identity column or sequence | `IDENTITY(1,1)` |
| Current date | `now()`, `CURRENT_DATE` | `NOW()` | `SYSDATE` | `GETDATE()` |
| Limit rows | `LIMIT n` | `LIMIT n` | `FETCH FIRST n ROWS ONLY` | `TOP n` |
| Modify column | `ALTER COLUMN … TYPE` | `MODIFY COLUMN` | `MODIFY` | `ALTER COLUMN` |

## 5.2 Creating a database

```text
CREATE DATABASE college;          -- PostgreSQL, MySQL, SQL Server
USE college;                      -- MySQL, SQL Server (in psql: \c college)
DROP DATABASE college;
```

Oracle has no `CREATE DATABASE` in everyday use; you work in a *schema* owned by a user (`CREATE USER college IDENTIFIED BY …`). Options at creation include character set, collation, file locations and size, which differ by product.

## 5.3 Data types

| Class | Types | Use |
|---|---|---|
| Exact numeric | `INT`, `SMALLINT`, `BIGINT`, `NUMERIC(p,s)` / `DECIMAL(p,s)` | counts, money (`NUMERIC(10,2)` = 8 digits before and 2 after the point) |
| Approximate | `REAL`, `DOUBLE PRECISION` | scientific values |
| Character | `CHAR(n)` fixed (padded), `VARCHAR(n)` variable | codes, names |
| Date/time | `DATE`, `TIME`, `TIMESTAMP` | dates of birth, logs |
| Boolean | `BOOLEAN` | flags |
| Large objects | `TEXT`, `BLOB`/`BYTEA` | documents, images |

## 5.4 Creating tables with constraints

`CREATE TABLE name (column type [constraints], …, [table constraints]);` Constraints:

| Constraint | Effect |
|---|---|
| `PRIMARY KEY` | unique and `NOT NULL`; one per table (may be composite, declared at table level) |
| `NOT NULL` | value required |
| `UNIQUE` | no duplicates (NULLs allowed) |
| `FOREIGN KEY … REFERENCES t(col)` | referential integrity; `ON DELETE CASCADE | SET NULL | RESTRICT` |
| `CHECK (condition)` | domain rule |
| `DEFAULT value` | value used when none is given |

```sql
CREATE TABLE department (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(40) NOT NULL UNIQUE
);
CREATE TABLE student (
    sid      INT PRIMARY KEY,
    name     VARCHAR(50) NOT NULL,
    email    VARCHAR(60) UNIQUE,
    dob      DATE,
    dept_id  INT REFERENCES department(dept_id) ON DELETE SET NULL,
    status   VARCHAR(10) DEFAULT 'active' CHECK (status IN ('active', 'passed', 'left'))
);
CREATE TABLE course (
    cid     CHAR(4) PRIMARY KEY,
    title   VARCHAR(60) NOT NULL,
    credits INT CHECK (credits BETWEEN 1 AND 6)
);
CREATE TABLE enrollment (
    sid   INT REFERENCES student(sid) ON DELETE CASCADE,
    cid   CHAR(4) REFERENCES course(cid),
    marks NUMERIC(5,2) CHECK (marks BETWEEN 0 AND 100),
    PRIMARY KEY (sid, cid)
);
```

**Constraints at work.** The statements below try to break each rule; the database rejects them and says why. `DEFAULT` fills the status automatically.

```sql
INSERT INTO department VALUES (10, 'BCA'), (20, 'BIT');
INSERT INTO student (sid, name, email, dept_id) VALUES (1, 'Sita', 'sita@example.np', 10);
INSERT INTO student (sid, name, dept_id) VALUES (2, 'Ram', 99);
INSERT INTO student (sid, name, email) VALUES (3, 'Hari', 'sita@example.np');
INSERT INTO student (sid, name) VALUES (1, 'Gita');
INSERT INTO student (sid, name, status) VALUES (4, 'Gita', 'retired');
INSERT INTO course VALUES ('C1', 'DBMS', 9);
SELECT sid, name, status FROM student;
```
```output
ERROR:  insert or update on table "student" violates foreign key constraint "student_dept_id_fkey"
DETAIL:  Key (dept_id)=(99) is not present in table "department".
ERROR:  duplicate key value violates unique constraint "student_email_key"
DETAIL:  Key (email)=(sita@example.np) already exists.
ERROR:  duplicate key value violates unique constraint "student_pkey"
DETAIL:  Key (sid)=(1) already exists.
ERROR:  new row for relation "student" violates check constraint "student_status_check"
DETAIL:  Failing row contains (4, Gita, null, null, null, retired).
ERROR:  new row for relation "course" violates check constraint "course_credits_check"
DETAIL:  Failing row contains (C1  , DBMS, 9).
 sid | name | status 
-----+------+--------
   1 | Sita | active
(1 row)
```

Read the messages: foreign key (no department 99), unique (duplicate e-mail), primary key (duplicate sid 1), check (status), check (credits). Only the first student row was stored, with `status = active` from the default.

## 5.5 Altering tables

`ALTER TABLE` changes the structure of an existing table without losing its data.

| Task | Syntax (PostgreSQL; Oracle/MySQL/SQL Server differences in 5.1) |
|---|---|
| Add a column | `ALTER TABLE t ADD COLUMN c type;` |
| Drop a column | `ALTER TABLE t DROP COLUMN c;` |
| Change type | `ALTER TABLE t ALTER COLUMN c TYPE type;` |
| Add a constraint | `ALTER TABLE t ADD CONSTRAINT name CHECK (…);` (or `UNIQUE`, `FOREIGN KEY`, `PRIMARY KEY`) |
| Drop a constraint | `ALTER TABLE t DROP CONSTRAINT name;` |
| Set / drop default | `ALTER COLUMN c SET DEFAULT v` / `DROP DEFAULT` |
| Rename | `ALTER TABLE t RENAME COLUMN a TO b;` · `ALTER TABLE t RENAME TO t2;` |

```sql
ALTER TABLE student ADD COLUMN phone VARCHAR(15);
ALTER TABLE student ALTER COLUMN name TYPE VARCHAR(80);
ALTER TABLE student ADD CONSTRAINT phone_len CHECK (length(phone) >= 7);
ALTER TABLE student DROP COLUMN dob;
ALTER TABLE student DROP CONSTRAINT phone_len;
SELECT column_name, data_type, character_maximum_length AS len
FROM information_schema.columns
WHERE table_schema = current_schema() AND table_name = 'student'
ORDER BY ordinal_position;
```
```output
 column_name |     data_type     | len 
-------------+-------------------+-----
 sid         | integer           |    
 name        | character varying |  80
 email       | character varying |  60
 dept_id     | integer           |    
 status      | character varying |  10
 phone       | character varying |  15
(6 rows)
```

Adding a `NOT NULL` column to a table that already has rows needs a `DEFAULT`, or the existing rows would violate it. The catalog query `information_schema.columns` is how a program reads the schema (metadata, Unit 1).

## 5.6 Dropping and truncating

- `DROP TABLE t;` removes the table and its data. It fails while another table's foreign key still refers to it; `DROP TABLE t CASCADE` removes the dependent constraints too.
- `TRUNCATE TABLE t;` removes **all rows** quickly but keeps the structure (DDL, usually cannot be rolled back in Oracle/MySQL). `DELETE FROM t;` removes rows one by one and can be rolled back (Unit 6).
- `DROP DATABASE d;` removes everything.

```sql
CREATE TABLE d1 (id INT PRIMARY KEY);
CREATE TABLE d2 (id INT, d1_id INT REFERENCES d1(id));
DROP TABLE d1;
DROP TABLE d1 CASCADE;
TRUNCATE TABLE d2;
DROP TABLE d2;
SELECT count(*) AS tables_left FROM information_schema.tables
WHERE table_schema = current_schema() AND table_name IN ('d1', 'd2');
```
```output
ERROR:  cannot drop table d1 because other objects depend on it
DETAIL:  constraint d2_d1_id_fkey on table d2 depends on table d1
HINT:  Use DROP ... CASCADE to drop the dependent objects too.
NOTICE:  drop cascades to constraint d2_d1_id_fkey on table d2
 tables_left 
-------------
           0
(1 row)
```

::: caution DROP, TRUNCATE and DELETE
`DROP` deletes structure and data; `TRUNCATE` deletes all data, keeps structure; `DELETE` deletes chosen rows, keeps structure and is transaction-safe. Always run `SELECT` with the same `WHERE` first.
:::

## Formula and fact sheet

- DDL: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`. Constraints: PRIMARY KEY, NOT NULL, UNIQUE, FOREIGN KEY, CHECK, DEFAULT.
- `NUMERIC(p, s)`: p total digits, s after the point.
- Foreign key actions: CASCADE, SET NULL, RESTRICT.
- `ALTER TABLE` can add/drop columns and constraints, change type, rename.

## Chapter summary

- SQL is declarative; DDL defines the schema, and constraints enforce integrity inside the database.
- Rejected statements show each constraint working; defaults supply missing values.
- `ALTER` evolves a table without data loss; `DROP` and `TRUNCATE` differ in how much they remove.

## Practice

1. Write `CREATE TABLE` for `book(isbn, title, price, copies)` with a primary key, a non-negative price and a default of 1 copy.
2. Create `member` and `loan` (member_id, isbn, issue_date) with foreign keys and a composite primary key.
3. Add an `email` column to `member`, make it unique, then drop it.
4. Explain `ON DELETE CASCADE` versus `SET NULL`.
5. Differentiate `DELETE`, `TRUNCATE` and `DROP`.
6. Why does `DROP TABLE department` fail when `student` refers to it?
7. Convert `VARCHAR(30)`, `INT`, `AUTO_INCREMENT` to Oracle types.

::: note Answers and worked solutions
**1.** `CREATE TABLE book (isbn CHAR(13) PRIMARY KEY, title VARCHAR(100) NOT NULL, price NUMERIC(8,2) CHECK (price >= 0), copies INT DEFAULT 1);`
**2.** `CREATE TABLE member (member_id INT PRIMARY KEY, name VARCHAR(50)); CREATE TABLE loan (member_id INT REFERENCES member, isbn CHAR(13) REFERENCES book, issue_date DATE, PRIMARY KEY (member_id, isbn, issue_date));`
**3.** `ALTER TABLE member ADD COLUMN email VARCHAR(60); ALTER TABLE member ADD CONSTRAINT uq_email UNIQUE (email); ALTER TABLE member DROP COLUMN email;` (dropping the column drops its constraint).
**4.** CASCADE deletes dependent rows with the parent; SET NULL keeps them and nulls the foreign key.
**5.** See the caution box: DELETE rows (rollback-able), TRUNCATE all rows (keeps table), DROP the table itself.
**6.** Dropping it would leave `student.dept_id` values pointing to nothing, breaking referential integrity; use CASCADE or drop `student` first.
**7.** `VARCHAR2(30)`, `NUMBER(10)`, and a sequence or identity column (`GENERATED ALWAYS AS IDENTITY`).
:::
