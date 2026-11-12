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

## 5.7 Seeing the ideas: constraints in action

Every statement in this section was run on a real PostgreSQL server, and the error messages quoted in the figures are the exact messages it printed. The test database has three tables: department(dept_id, dept_name), student(sid, name, email, dob, dept_id, status) and enrollment(sid, cid, marks) with the composite key (sid, cid).

```svgfig label="5.1" caption="Anatomy of a CREATE TABLE statement. Each coloured tag points to the part of the statement that creates one kind of rule. Column constraints (written after one column) govern that column; table constraints (written after all columns) can involve several columns, such as the composite primary key (sid, cid) of enrollment. The DBMS stores all these rules in the data dictionary and checks them on every INSERT, UPDATE and DELETE."
f = Fig(580, 270)
f.box(10, 10, 350, 250, "", fill=SOFT, stroke=SLATE, sw=1.2)
code = ["CREATE TABLE student (", "  sid     INT PRIMARY KEY,", "  name    VARCHAR(40) NOT NULL,", "  email   VARCHAR(60) UNIQUE,", "  dob     DATE,", "  dept_id INT REFERENCES", "          department(dept_id)", "          ON DELETE SET NULL,", "  status  VARCHAR(10) DEFAULT 'active'", "          CHECK (status IN", "          ('active','passed','left'))", ");"]
for i, ln in enumerate(code):
    f.text(20, 30 + i * 18.5, ln, size=10.5, color=NAVY, anchor="start", bold=(i in (0, 11)))
tags = [(48, "primary key: unique + not null", TEAL), (67, "required value", TEAL), (86, "no duplicates (NULL allowed)", TEAL), (141, "foreign key: must exist in department", RED), (159, "delete action", RED), (178, "default used when omitted", AMBER), (197, "domain rule", AMBER)]
for y, s, c in tags:
    f.arrow([(520 - 150, y - 3), (366, y - 3)], color=c, sw=1.1)
    f.text(374, y - 12, s, size=9.5, color=c, bold=True, anchor="start")
f.text(470, 250, "real PostgreSQL syntax", size=9.5, color=SLATE, bold=True)
```

```svgfig label="5.2" caption="Six bad INSERT statements and what PostgreSQL did with each. Every one was refused and no row was stored, because each broke a declared rule. The right-hand column quotes the first line of the real error message. Constraints therefore protect the data even when a careless program or a typing error produces wrong values."
f = Fig(580, 290)
rows = [
 ("INSERT student (4, 'Mina', 'sita@x.np', 10)", "duplicate key value violates unique constraint \"student_email_key\"", "UNIQUE"),
 ("INSERT student (5, 'Mina', dept_id 99)", "violates foreign key constraint \"student_dept_id_fkey\"", "FOREIGN KEY"),
 ("INSERT student (1, 'Dup')", "duplicate key value violates unique constraint \"student_pkey\"", "PRIMARY KEY"),
 ("INSERT student (6, 'Gita', status 'gone')", "violates check constraint \"student_status_check\"", "CHECK"),
 ("INSERT enrollment (1, 'C3', marks 150)", "violates check constraint \"enrollment_marks_check\"", "CHECK"),
 ("INSERT student (7, name NULL)", "null value in column \"name\" violates not-null constraint", "NOT NULL"),
]
f.box(6, 8, 230, 22, "Statement attempted", fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=0)
f.box(236, 8, 270, 22, "PostgreSQL answer (first line)", fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=0)
f.box(506, 8, 70, 22, "Rule", fill=NAVY, stroke=NAVY, color="#ffffff", size=10, bold=True, r=0)
for i, (a, b, c) in enumerate(rows):
    y = 30 + i * 38
    fl = ROSE if i % 2 == 0 else SOFT
    f.box(6, y, 230, 38, a.replace(" (", "\n("), fill=fl, stroke=SLATE, size=9, r=0)
    f.box(236, y, 270, 38, b.replace(" violates", "\nviolates").replace(" value in", "\nvalue in") if len(b) > 50 else b, fill=fl, stroke=SLATE, size=8.5, r=0, color=RED)
    f.box(506, y, 70, 38, c, fill=fl, stroke=SLATE, size=8.5, r=0, bold=True, color=NAVY)
f.text(290, 278, "result for all six: 0 rows inserted, database unchanged", size=10.5, color=TEAL, bold=True)
```

```svgfig label="5.3" caption="The ON DELETE actions, shown with real results. Before the deletes, department 10 (BCA) has students Sita and Ram, and Sita has two enrolment rows. With ON DELETE SET NULL on student.dept_id, deleting BCA succeeded and both students stayed with dept_id NULL. With ON DELETE CASCADE on enrollment.sid, deleting Sita also deleted her two enrolment rows (the count fell from 2 to 0). With RESTRICT or NO ACTION the delete would have been refused while child rows exist."
f = Fig(580, 234)
f.text(100, 12, "SET NULL", size=11, color=AMBER, bold=True)
f.box(10, 22, 180, 24, "DELETE department 10", fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(10, 60, 85, 24, "1 Sita | 10", fill=BLUE, stroke=NAVY, size=9.5, r=0)
f.box(10, 84, 85, 24, "2 Ram | 10", fill=BLUE, stroke=NAVY, size=9.5, r=0)
f.arrow([(100, 84), (115, 84)], color=SLATE, sw=1.5)
f.box(120, 60, 70, 24, "1 Sita | NULL", fill=MINT, stroke=TEAL, size=9, r=0)
f.box(120, 84, 70, 24, "2 Ram | NULL", fill=MINT, stroke=TEAL, size=9, r=0)
f.text(100, 130, "children kept, link cleared", size=9.5, color=SLATE, bold=True)
f.text(300, 12, "CASCADE", size=11, color=RED, bold=True)
f.box(210, 22, 180, 24, "DELETE student 1 (Sita)", fill=ROSE, stroke=RED, size=10, bold=True)
f.box(210, 60, 85, 24, "(1, C1, 85)", fill=BLUE, stroke=NAVY, size=9.5, r=0)
f.box(210, 84, 85, 24, "(1, C2, 72)", fill=BLUE, stroke=NAVY, size=9.5, r=0)
f.arrow([(300, 84), (315, 84)], color=SLATE, sw=1.5)
f.box(320, 66, 70, 36, "0 rows\nleft", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.text(300, 130, "children deleted with parent", size=9.5, color=SLATE, bold=True)
f.text(490, 12, "RESTRICT / NO ACTION", size=11, color=NAVY, bold=True)
f.box(410, 22, 170, 24, "DELETE department 10", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(410, 60, 170, 48, "refused: students still\nreference department 10", fill=ROSE, stroke=RED, size=10, bold=True)
f.text(495, 130, "parent is protected", size=9.5, color=SLATE, bold=True)
f.box(10, 160, 560, 62, "Choose by meaning:\nSET NULL for an optional link (a student may have no department yet)\nCASCADE for a part that cannot exist alone (enrolment rows of a deleted student)\nRESTRICT when deletion is probably a mistake (a department that still has students)", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
```

```svgfig label="5.4" caption="What each statement removes. DELETE removes chosen rows and can use WHERE; the table, its columns and its constraints stay, and a transaction can undo it. TRUNCATE removes all rows quickly and keeps the table definition; it takes no WHERE clause. DROP TABLE removes the rows and the table itself, including its indexes and constraints. ALTER TABLE changes the structure (add, drop or change a column, add or drop a constraint) and keeps the data. In PostgreSQL even TRUNCATE and DROP can be rolled back inside a transaction, whereas MySQL and Oracle commit implicitly after DDL statements."
f = Fig(580, 200)
hdr = ["", "Rows", "Table structure", "WHERE allowed", "Undo (ROLLBACK)"]
xs = [6, 96, 186, 316, 436]
ws = [90, 90, 130, 120, 138]
data = [("DELETE", "chosen rows", "kept", "yes", "yes"), ("TRUNCATE", "all rows", "kept", "no", "PostgreSQL yes; MySQL no"), ("DROP TABLE", "all rows", "removed", "no", "PostgreSQL yes; MySQL no"), ("ALTER TABLE", "kept", "changed", "no", "PostgreSQL yes; MySQL no")]
for j, h in enumerate(hdr):
    f.box(xs[j], 8, ws[j], 24, h, fill=NAVY, stroke=NAVY, color="#ffffff", size=9.5, bold=True, r=0)
for i, row in enumerate(data):
    for j, v in enumerate(row):
        f.box(xs[j], 32 + i * 34, ws[j], 34, v.replace("; ", ";\n"), fill=(BLUE if i % 2 == 0 else SOFT), stroke=NAVY, size=9, r=0, bold=(j == 0))
f.text(290, 188, "DDL = CREATE, ALTER, DROP, TRUNCATE      DML = INSERT, UPDATE, DELETE, SELECT", size=10, color=SLATE, bold=True)
```

### 5.7.1 Eight advantages of declaring constraints in the table definition

1. **Rules are written once.** A rule such as marks between 0 and 100 is part of the table and applies to every program that uses it. Without it, each program, from the clerk's data-entry screen to the import tool, would need its own check. One definition is easier to read, to test and to change.
2. **Bad data is stopped at the door.** As Figure 5.2 shows, wrong values are refused at the moment of insertion with a clear message. It is much cheaper to refuse a mark of 150 than to find and correct it after results have been printed. Clean data means trustworthy reports.
3. **Duplicates are impossible.** A primary key or UNIQUE rule stops two students from sharing a roll number or an email address. This holds even when two clerks save a record at the same moment, because the DBMS itself checks. A manual search for duplicates is no longer needed.
4. **Links between tables stay valid.** A foreign key guarantees that every enrolment belongs to a real student and every student belongs to a real department. No orphan rows can appear. Joins therefore never lose rows because of broken links.
5. **Deletions behave in a planned way.** ON DELETE CASCADE, SET NULL or RESTRICT decides in advance what happens to dependent rows (Figure 5.3). The designer thinks about it once, and the database then behaves the same way for every user. Accidental loss of important parents is prevented.
6. **Defaults save typing and mistakes.** A DEFAULT value such as status 'active' or the current date is filled in when no value is given. Data-entry staff type less and forget fewer fields. Every row starts in a sensible state.
7. **The schema documents itself.** Reading the CREATE TABLE statement tells a new team member the keys, the allowed values and the links between tables. The data dictionary can also be queried by tools. Documentation can never be out of date, because it is the definition itself.
8. **Queries and the optimiser benefit.** Knowing that a column is unique or not null lets the optimiser choose faster plans, and primary and unique keys automatically get an index. A lookup by sid is quick without extra work. Good constraints therefore improve speed as well as correctness.

## 5.8 Seeing the ideas with photographs: SQL, storage and removal

SQL was designed in the early 1970s at IBM, and nearly every statement in this unit descends from that work. The plates below put real numbers on two choices a student makes in every CREATE TABLE and every clean-up: how big a data type is, and what DELETE, TRUNCATE and DROP really do to the disk. All numbers were measured on PostgreSQL 15.

```photogrid label="5.1" cols="2" ratio="1.4" caption="Choosing a data type is choosing bytes. (a) Donald D. Chamberlin, who with Raymond Boyce designed SQL (first called SEQUEL) at IBM. (b) The size in bytes of single values measured with pg_column_size() on PostgreSQL 15: SMALLINT 2, BOOLEAN 1, INT and DATE 4, BIGINT and TIMESTAMP 8, NUMERIC(10,2) 12, UUID 16. Text types add a 4-byte header to the characters, and a Devanagari word costs 3 bytes per letter in UTF-8: the eight letters of the word for Kathmandu take 24 bytes, so 28 with the header, against 13 for the nine-letter English word."
@ photo id="bca202/chamberlin" cap="Donald D. Chamberlin, co-designer of SQL"
fit 1.4
focus 0.5 0.75
@ svg cap="Bytes per value (measured)"
meas = [("BOOLEAN true", 1), ("SMALLINT", 2), ("INT", 4), ("DATE", 4), ("BIGINT", 8), ("TIMESTAMP", 8), ("NUMERIC(10,2)", 12), ("'Kathmandu' TEXT", 13), ("UUID", 16), ("Devanagari word TEXT", 28)]
d = dict(meas)
assert d["Devanagari word TEXT"] == 8 * 3 + 4 and d["'Kathmandu' TEXT"] == 9 + 4 and len("काठमाडौं".encode("utf-8")) == 24
f = Fig(300, 262)
f.text(150, 11, "bytes of one value, PostgreSQL 15", size=10, color=NAVY, bold=True)
for i, (k, v) in enumerate(meas):
    y = 24 + i * 23
    col = AMBER if "TEXT" in k else TEAL
    f.text(6, y + 8, k, size=9.5, color=SLATE, bold=True, anchor="start")
    f.box(124, y, v * 5.6, 15, "", fill=col, stroke=col, r=2)
    f.text(124 + v * 5.6 + 5, y + 8, str(v), size=10, color=col, bold=True, anchor="start")
f.text(150, 256, "text = 4-byte header + UTF-8 bytes of the letters", size=9.5, color=AMBER, bold=True)
```

```photogrid label="5.2" cols="2" ratio="1.1" caption="Three ways to remove data. (a) The cutting blades of a paper shredder: once shredded, a page cannot be put back, which is how DROP behaves outside a transaction. (b) A table of 50,000 rows occupied 5,398,528 bytes. DELETE FROM removed every row, but the file stayed 5,398,528 bytes (the dead rows wait for VACUUM); VACUUM then shrank it to 1,163,264 bytes (the primary-key index remains); TRUNCATE cut it to 16,384 bytes at once; DROP TABLE removed it entirely. Inside a transaction, DELETE and TRUNCATE were both rolled back on PostgreSQL and all 50,000 rows came back."
@ photo id="bca202/shredder" cap="Paper shredder blades"
fit 1.1
focus 0.5 0.5
@ svg cap="Table size after each statement"
steps = [("before", 5398528), ("DELETE", 5398528), ("DELETE + VACUUM", 1163264), ("TRUNCATE", 16384), ("DROP TABLE", 0)]
f = Fig(300, 250)
f.text(150, 11, "bytes on disk (50,000-row table)", size=10, color=NAVY, bold=True)
for i, (k, v) in enumerate(steps):
    y = 26 + i * 34
    w = 190 * v / 5398528
    col = SLATE if i < 2 else (AMBER if i < 4 else RED)
    f.text(6, y + 8, k, size=9.5, color=SLATE, bold=True, anchor="start")
    f.box(104, y, max(w, 2), 16, "", fill=col, stroke=col, r=2)
    f.text(104 + max(w, 2) + 5, y + 9, "{:,}".format(v), size=9.5, color=col, bold=True, anchor="start")
assert steps[0][1] == steps[1][1]
f.box(6, 200, 288, 40, "in a transaction: ROLLBACK after DELETE or\nTRUNCATE brings back all 50,000 rows (PostgreSQL)", fill=SAND, stroke=AMBER, size=9.5, bold=True)
```

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

## Model answers (5 and 10 marks)

**Q1 (5 marks). Differentiate between DROP, TRUNCATE and DELETE.**

*Introduction.* All three remove data, but they remove different things and belong to different SQL groups. DELETE is a DML statement, while DROP and TRUNCATE are DDL statements (Figure 5.4).

1. **DELETE.** It removes the rows chosen by the WHERE clause, or all rows if there is no WHERE. For example `DELETE FROM student WHERE sid = 3;` removes one student. The table, its columns and its constraints remain, and the action is logged row by row, so it can be rolled back and can fire triggers.
2. **TRUNCATE.** It removes all rows at once, quickly, and resets storage. `TRUNCATE enrollment;` empties the table but keeps its definition. It has no WHERE clause and does not fire row-level delete triggers.
3. **DROP.** It removes the whole table, including rows, columns, indexes and constraints: `DROP TABLE student;`. The table no longer exists, and any foreign key that refers to it makes the statement fail unless `CASCADE` is added.
4. **Transactions.** In MySQL and Oracle, DDL statements commit implicitly and cannot be rolled back. PostgreSQL allows DDL inside a transaction, so TRUNCATE and DROP can be undone there.
5. **When to use.** Use DELETE to remove some rows, TRUNCATE to empty a table for reuse, and DROP when the table is no longer needed.

*Conclusion.* DELETE trims the data, TRUNCATE empties the table and DROP removes the table itself.

**Q2 (5 marks). What are SQL constraints? Write a CREATE TABLE statement that uses them.**

*Introduction.* Constraints are rules attached to a table so that the DBMS itself keeps the data valid. The types are PRIMARY KEY, NOT NULL, UNIQUE, FOREIGN KEY, CHECK and DEFAULT (Figure 5.1).

```sql
CREATE TABLE student (
    sid     INT PRIMARY KEY,
    name    VARCHAR(40) NOT NULL,
    email   VARCHAR(60) UNIQUE,
    dept_id INT REFERENCES department(dept_id) ON DELETE SET NULL,
    status  VARCHAR(10) DEFAULT 'active'
            CHECK (status IN ('active','passed','left'))
);
```

1. **PRIMARY KEY** makes sid unique and not null; each table has one, which may be composite.
2. **NOT NULL** forces a name to be given.
3. **UNIQUE** forbids two students with the same email, but allows several NULLs.
4. **FOREIGN KEY ... REFERENCES** forces dept_id to exist in department; `ON DELETE SET NULL` clears it if the department is deleted.
5. **CHECK** limits status to three values, and **DEFAULT** supplies 'active' when no value is given.

*Test.* On a real server, inserting a second student with email sita@x.np failed with "duplicate key value violates unique constraint", and a status of 'gone' failed with "violates check constraint".

*Conclusion.* Declared constraints guard every insert and update, whichever program sends it.

**Q3 (10 marks). Write SQL statements to create the tables department, student and enrollment with suitable constraints. Then add a column, change its type, and explain ON DELETE CASCADE and SET NULL with the result of deleting a department and a student.**

*Introduction.* SQL has data definition statements, `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, that build and change the structure, and data manipulation statements that handle rows. We define the tables of the college database with their keys and rules first.

```sql
CREATE TABLE department (
    dept_id   INT PRIMARY KEY,
    dept_name VARCHAR(40) NOT NULL UNIQUE
);
CREATE TABLE student (
    sid     INT PRIMARY KEY,
    name    VARCHAR(40) NOT NULL,
    dept_id INT REFERENCES department(dept_id) ON DELETE SET NULL
);
CREATE TABLE enrollment (
    sid   INT REFERENCES student(sid) ON DELETE CASCADE,
    cid   VARCHAR(8),
    marks INT CHECK (marks BETWEEN 0 AND 100),
    PRIMARY KEY (sid, cid)
);
```

*Design choices.* The order of creation matters: department first, then student, then enrollment, because a foreign key can refer only to an existing table. Enrollment has a composite primary key because the pair (sid, cid) identifies one enrolment.

*Altering.* The structure is changed without losing data:

```sql
ALTER TABLE student ADD COLUMN phone VARCHAR(15);
ALTER TABLE student ALTER COLUMN name TYPE VARCHAR(60);
ALTER TABLE student RENAME COLUMN phone TO mobile;
```

*Referential actions.* With department rows (10, BCA) and (20, BIT), students Sita and Ram in 10 and Hari in 20, and two enrolments of Sita, we ran the deletes on a real server.
1. `DELETE FROM department WHERE dept_id = 10;` succeeded, and Sita and Ram stayed with dept_id NULL because of `ON DELETE SET NULL`.
2. `DELETE FROM student WHERE sid = 1;` removed Sita, and her two enrollment rows disappeared too (the count fell from 2 to 0) because of `ON DELETE CASCADE`.
3. Without these clauses the default NO ACTION refuses the delete while child rows exist.

| Action | Effect on child rows | Typical use |
|---|---|---|
| CASCADE | deleted with the parent | enrolments of a student |
| SET NULL | foreign key becomes NULL | optional link such as department |
| RESTRICT / NO ACTION | delete refused | protect important parents |

*Conclusion.* DDL statements define the structure and the rules; ON DELETE actions let the designer decide, once, how deletions spread, so the database stays consistent without extra program code.
