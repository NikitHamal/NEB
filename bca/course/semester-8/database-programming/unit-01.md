---
subject: Database Programming
grade: BCA Semester 8 (Elective III)
unit: 1
title: Introduction of RDBMS
hours: 10
area: BCA 453 · Database Programming · Unit 1
---

A college in Butwal keeps its results in an Oracle database. At 9 a.m. on result day, two thousand students open the portal at once, a clerk fixes a wrong mark, and the principal runs a report, all at the same time and without anyone seeing half-finished data. None of this is done by the portal's screens. It is done by the database itself, through programs that live **inside** it: SQL statements, PL/SQL blocks, triggers, procedures and packages. This course teaches you to write those programs for the Oracle relational database.

Your DBMS course (BCA 255, Unit 7 there) introduced stored procedures and triggers in a general way. Here we use the Oracle dialect throughout, because the TU outline is built on Oracle: SQL*Plus, PL/SQL, cursors, triggers, records, procedures, functions and packages. This first unit gets you ready: how Oracle is built, how to work in SQL*Plus, and a fast, complete revision of the SQL you will call from PL/SQL.

::: key What this unit gives you
- The Oracle architecture: instance, database, memory structures, background processes and storage structures.
- SQL*Plus: connecting, DESCRIBE, the buffer commands (LIST, APPEND, CHANGE, INPUT, DEL, CLEAR BUFFER), script files and runtime values with `&`.
- A working revision of DDL, DML, DCL, joins and subqueries on the classic EMP and DEPT tables used in every later unit.
:::

## 1.1 Overview of the Oracle Database architecture

An **Oracle database server** consists of two things that people often confuse.

- The **database** is the set of files on disk: data files, control files and redo log files.
- The **instance** is the set of memory structures and background processes that run on the server and work on those files.

When you "start Oracle", you start an instance, which then **mounts** and **opens** the database. One instance serves one database (in a single-instance installation), and every user session connects to the instance, never directly to the files.

**Memory structures**

| Area | What it holds | Purpose |
|---|---|---|
| **SGA** (System Global Area) | Shared by all sessions; created at instance start | The central working memory |
| Database buffer cache (in the SGA) | Copies of data blocks read from the data files | Avoids disk reads for popular rows |
| Shared pool (in the SGA) | Parsed SQL and PL/SQL, the data dictionary cache | A statement that was parsed once is reused |
| Redo log buffer (in the SGA) | A record of every change made | Written to disk at commit, for recovery |
| **PGA** (Program Global Area) | Private to one server process | Sorting, session variables, cursor state |

**Background processes** do the housekeeping:

| Process | Job |
|---|---|
| **DBWn** (database writer) | Writes modified ("dirty") blocks from the buffer cache to the data files |
| **LGWR** (log writer) | Writes the redo log buffer to the online redo log files, and always at COMMIT |
| **CKPT** (checkpoint) | Marks a point up to which all changes are in the data files, so recovery starts there |
| **SMON** (system monitor) | Performs instance recovery after a crash |
| **PMON** (process monitor) | Cleans up after failed sessions, releasing their locks |
| **ARCn** (archiver) | Copies filled redo logs to archive storage, when archiving is on |

**Physical storage** is made of three file types. **Data files** hold tables and indexes. **Redo log files** hold the change history. **Control files** are small files that record the structure of the database (names and places of all the other files).

**Logical storage** is how Oracle organises the same space for you:

> tablespace $\rightarrow$ segment $\rightarrow$ extent $\rightarrow$ data block

A **tablespace** (for example SYSTEM, SYSAUX, USERS, TEMP, UNDO) is a named group of data files. A **segment** is the space for one object, such as a table or an index. An **extent** is a set of contiguous blocks given to a segment at once, and a **data block** (usually 8 KB) is the smallest unit of I/O. A **schema** is the collection of objects (tables, views, procedures, packages) owned by one user, and the **data dictionary** is a set of read-only tables and views (`USER_TABLES`, `USER_SOURCE`, `USER_ERRORS` and so on) where Oracle describes everything in the database. You will query it often, for example to see PL/SQL compile errors.

```svgfig label="1.1" caption="Oracle instance and database. Sessions talk to server processes; the SGA caches data and SQL; background processes move data between the SGA and the files."
f = Fig(640, 300)
f.box(10, 10, 130, 40, "User session\nSQL*Plus / app", fill=SOFT, stroke=SLATE, size=9.5)
f.box(10, 70, 130, 40, "Server process\n(with its PGA)", fill=BLUE, stroke=NAVY, size=9.5)
f.arrow([(75, 50), (75, 70)], color=NAVY)
f.box(170, 10, 300, 150, "", fill=SAND, stroke=AMBER)
f.text(320, 24, "INSTANCE: SGA in memory", size=10, anchor="middle", color=AMBER)
f.box(180, 36, 135, 44, "Database\nbuffer cache", fill="#ffffff", stroke=AMBER, size=9.5)
f.box(325, 36, 135, 44, "Shared pool\nSQL, PL/SQL, dictionary", fill="#ffffff", stroke=AMBER, size=8.5)
f.box(180, 92, 135, 44, "Redo log\nbuffer", fill="#ffffff", stroke=AMBER, size=9.5)
f.box(325, 92, 135, 44, "Background:\nDBWn LGWR CKPT\nSMON PMON", fill=MINT, stroke=TEAL, size=8.5)
f.arrow([(140, 90), (170, 90)], color=NAVY)
f.box(170, 200, 300, 90, "", fill=MINT, stroke=TEAL)
f.text(320, 214, "DATABASE: files on disk", size=10, anchor="middle", color=TEAL)
f.box(180, 226, 90, 52, "Data files\n(tablespaces)", fill="#ffffff", stroke=TEAL, size=9)
f.box(280, 226, 90, 52, "Redo log\nfiles", fill="#ffffff", stroke=TEAL, size=9)
f.box(380, 226, 80, 52, "Control\nfiles", fill="#ffffff", stroke=TEAL, size=9)
f.arrow([(247, 160), (247, 226)], color=TEAL, label="DBWn", lpos=(272, 195))
f.arrow([(325, 160), (325, 226)], color=TEAL, label="LGWR", lpos=(350, 195))
```

**How one statement runs.** For `UPDATE emp SET sal = sal + 100 WHERE empno = 7369;` the server process (1) parses the statement, reusing a cached version from the shared pool if the same text came before; (2) finds the block holding the row, reading it into the buffer cache if it is not there; (3) records the change in the redo log buffer and in undo; (4) changes the block in the cache. Nothing is yet permanent. On `COMMIT`, LGWR writes the redo to disk and the change is durable; DBWn writes the data block later, in its own time. This **write-ahead** design is why Oracle can recover committed work after a crash.

::: note Why PL/SQL is fast
A PL/SQL block runs **inside** the instance, next to the data. A loop that updates 10,000 rows from PL/SQL makes no network round trips, while the same loop in a client program may make 10,000. The shared pool also keeps compiled PL/SQL, so a stored procedure is parsed once and reused by every session.
:::

## 1.2 Getting familiar with SQL*Plus

**SQL*Plus** is Oracle's command-line client. It runs three kinds of input: SQL statements, PL/SQL blocks, and its own **SQL*Plus commands**. The difference matters.

| | SQL statement / PL/SQL block | SQL*Plus command |
|---|---|---|
| Examples | `SELECT`, `UPDATE`, `BEGIN ... END;` | `DESCRIBE`, `SET`, `LIST`, `SPOOL` |
| Sent to the server? | Yes | No, handled by the client |
| Stored in the SQL buffer? | Yes (the last one) | No |
| Terminator | `;` for SQL, `/` for PL/SQL | None needed (a `;` is allowed) |

**Connecting.** From the operating-system prompt:

```sqlplus
sqlplus scott/tiger@localhost:1521/XEPDB1
SQL> SHOW USER
USER is "SCOTT"
```

(`scott` is a demo user; on Oracle XE you create your own user and grant it `CONNECT` and `RESOURCE`. Never use real passwords on the command line in practice: type `sqlplus scott@...` and SQL*Plus asks for the password without echoing.)

**DESCRIBE** (abbreviated `DESC`) shows the structure of a table, view, procedure or function:

```sqlplus
SQL> DESCRIBE dept
 Name                  Null?    Type
 --------------------- -------- ------------------
 DEPTNO                NOT NULL NUMBER(2)
 DNAME                          VARCHAR2(14)
 LOC                            VARCHAR2(13)
```

**Useful SET and formatting commands**

| Command | Effect |
|---|---|
| `SET LINESIZE 120` | Width of a line of output, to stop wrapping |
| `SET PAGESIZE 50` | Lines per page before the column headings repeat |
| `SET SERVEROUTPUT ON` | Shows what `DBMS_OUTPUT.PUT_LINE` prints (off by default, a common surprise in the lab) |
| `SET VERIFY OFF` | Hides the "old/new" lines when `&` variables are substituted |
| `SET TIMING ON` | Prints elapsed time for each statement |
| `COLUMN ename FORMAT A12` | Width of a text column |
| `COLUMN sal FORMAT 99,999.99` | Number format with a comma and two decimals |
| `SHOW ERRORS` | Lists compile errors of the last PL/SQL unit |

## 1.3 SQL*Plus buffer commands

SQL*Plus keeps the **last SQL statement or PL/SQL block** you typed in the **SQL buffer**. The editing commands work on this buffer, one line at a time, and let you fix a long statement without retyping it. Each command has a short form.

| Command | Short | What it does |
|---|---|---|
| `LIST` | `L` | Shows all buffer lines with numbers; the **current line** is marked with `*` |
| `LIST n` | `L n` | Shows line *n* and makes it the current line |
| `APPEND text` | `A text` | Adds *text* at the end of the current line |
| `CHANGE /old/new/` | `C /old/new/` | Replaces the first *old* with *new* in the current line |
| `INPUT text` | `I text` | Inserts a new line after the current line |
| `DEL` | none | Deletes the current line; `DEL n` deletes line *n*, `DEL m n` a range |
| `CLEAR BUFFER` | `CL BUFF` | Empties the buffer |
| `RUN` or `/` | `R` | Runs the buffer (`RUN` also displays it; `/` does not) |

A complete session on the EMP table (described in Section 1.6):

```sqlplus
SQL> SELECT ename, sal
  2  FROM emp
  3  WHERE deptno = 10;

ENAME             SAL
---------- ----------
CLARK            2450
KING             5000
MILLER           1300

SQL> LIST
  1  SELECT ename, sal
  2  FROM emp
  3* WHERE deptno = 10

SQL> CHANGE /10/20/
  3* WHERE deptno = 20
SQL> APPEND  AND sal > 2000
  3* WHERE deptno = 20 AND sal > 2000
SQL> INPUT ORDER BY sal DESC
SQL> LIST
  1  SELECT ename, sal
  2  FROM emp
  3  WHERE deptno = 20 AND sal > 2000
  4* ORDER BY sal DESC
SQL> /

ENAME             SAL
---------- ----------
SCOTT            3000
FORD             3000
JONES            2975

SQL> DEL 4
SQL> LIST
  1  SELECT ename, sal
  2  FROM emp
  3* WHERE deptno = 20 AND sal > 2000
SQL> CLEAR BUFFER
buffer cleared
```

Four points deserve care. (1) The trailing `;` is **not** stored in the buffer, which is why `LIST` shows line 3 without it. (2) `APPEND` keeps the text exactly as typed after the first space, so to get a space between `deptno = 20` and `AND` you type **two** spaces after the word `APPEND`. (3) `CHANGE` works only on the **current** line, so after `LIST` (current line is the last) you must `LIST 3` first if you want to edit an earlier line. (4) A PL/SQL block ends with `.` on a line by itself (keeps the block in the buffer without running it) or `/` (runs it).

## 1.4 Script files

Anything you will run more than once belongs in a **script file**, a plain text file (conventionally `.sql`).

| Command | Purpose |
|---|---|
| `SAVE file` | Writes the buffer to `file.sql` (`SAVE file REPLACE` overwrites, `APPEND` adds) |
| `GET file` | Loads a script into the buffer without running it |
| `START file` or `@file` | Loads and runs the script (`@@file` runs a script from the same folder as the calling script) |
| `EDIT file` | Opens the file in the operating-system editor |
| `SPOOL file` ... `SPOOL OFF` | Copies everything shown on the screen into `file.lst` |
| `HOST command` | Runs an operating-system command |
| `REM` or `--` | A comment line |

A tidy lab script, saved as `report10.sql`:

```sqlplus
REM report10.sql: salary report for one department
SET PAGESIZE 20
SET LINESIZE 80
SET VERIFY OFF
COLUMN ename  HEADING 'Employee'   FORMAT A10
COLUMN sal    HEADING 'Salary'     FORMAT 99,999
SPOOL report10.lst
SELECT ename, job, sal
FROM   emp
WHERE  deptno = 10
ORDER  BY sal DESC;
SPOOL OFF
```

Running `@report10` prints the report, saves a copy in `report10.lst` and leaves the SQL buffer holding the SELECT. Such files are also how you keep your PL/SQL programs in the lab: write the block in an editor, save it as `prog1.sql`, run it with `@prog1`, and fix it with `EDIT prog1` when the compiler complains.

## 1.5 Accepting values at runtime

A **substitution variable** is a name preceded by `&`. Before sending the statement to the server, SQL*Plus replaces it by a value it asks you for.

```sqlplus
SQL> SET VERIFY ON
SQL> SELECT ename, sal FROM emp WHERE deptno = &dno;
Enter value for dno: 10
old   1: SELECT ename, sal FROM emp WHERE deptno = &dno
new   1: SELECT ename, sal FROM emp WHERE deptno = 10

ENAME             SAL
---------- ----------
CLARK            2450
KING             5000
MILLER           1300
```

Rules to remember:

1. **Numbers** are substituted as they are; **text and dates** need quotes, so write `WHERE job = '&job'`. Without the quotes `CLERK` is read as a column name and gives `ORA-00904: "CLERK": invalid identifier`.
2. A **double ampersand** `&&dno` asks once and keeps the value for the rest of the session (it defines the variable). A single `&` asks every time it appears.
3. `DEFINE var = value` sets a variable yourself; `DEFINE` alone lists them; `UNDEFINE var` removes one.
4. `ACCEPT` gives a nicer prompt and checks the type:

```sqlplus
ACCEPT v_dno NUMBER PROMPT 'Department number: '
ACCEPT v_name CHAR PROMPT 'Employee name (capitals): '
SELECT empno, ename, sal FROM emp
WHERE  deptno = &v_dno AND ename LIKE '&v_name%';
```

5. `PROMPT text` prints a message and `PAUSE` waits for Enter; both are useful in scripts.

Substitution is a **client-side text replacement**, done before the server sees anything. In PL/SQL you will use it to hand a value into an anonymous block (Unit 2): `v_empno := &empno;` becomes `v_empno := 7369;` before the block is compiled. It is not a bind variable, and it is the reason user input through `&` must never be trusted in real applications (the text can contain anything, including more SQL).

## 1.6 The sample schema: EMP and DEPT

Every example in this book uses the two classic Oracle demo tables, so that you can type them into your own lab database. **DEPT** has four rows and **EMP** fourteen. Columns of EMP: `EMPNO` (key), `ENAME`, `JOB`, `MGR` (the manager's EMPNO), `HIREDATE`, `SAL`, `COMM` (commission, often NULL) and `DEPTNO` (foreign key to DEPT).

The program below builds the same data in an in-memory database and prints it. We use Python's `sqlite3` module here only so that the output is real and reproducible; the statements are standard SQL and the same text works in SQL*Plus (apart from the `(+)` and `NVL` forms shown as Oracle code later).

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE dept (deptno INTEGER PRIMARY KEY, dname TEXT, loc TEXT);
INSERT INTO dept VALUES (10,'ACCOUNTING','NEW YORK'),(20,'RESEARCH','DALLAS'),(30,'SALES','CHICAGO'),(40,'OPERATIONS','BOSTON');
CREATE TABLE emp (empno INTEGER PRIMARY KEY, ename TEXT, job TEXT, mgr INTEGER, hiredate TEXT, sal INTEGER, comm INTEGER, deptno INTEGER REFERENCES dept);
INSERT INTO emp VALUES
(7369,'SMITH','CLERK',7902,'1980-12-17',800,NULL,20),(7499,'ALLEN','SALESMAN',7698,'1981-02-20',1600,300,30),
(7521,'WARD','SALESMAN',7698,'1981-02-22',1250,500,30),(7566,'JONES','MANAGER',7839,'1981-04-02',2975,NULL,20),
(7654,'MARTIN','SALESMAN',7698,'1981-09-28',1250,1400,30),(7698,'BLAKE','MANAGER',7839,'1981-05-01',2850,NULL,30),
(7782,'CLARK','MANAGER',7839,'1981-06-09',2450,NULL,10),(7788,'SCOTT','ANALYST',7566,'1987-04-19',3000,NULL,20),
(7839,'KING','PRESIDENT',NULL,'1981-11-17',5000,NULL,10),(7844,'TURNER','SALESMAN',7698,'1981-09-08',1500,0,30),
(7876,'ADAMS','CLERK',7788,'1987-05-23',1100,NULL,20),(7900,'JAMES','CLERK',7698,'1981-12-03',950,NULL,30),
(7902,'FORD','ANALYST',7566,'1981-12-03',3000,NULL,20),(7934,'MILLER','CLERK',7782,'1982-01-23',1300,NULL,10);
""")
def show(sql):
    cur = db.execute(sql)
    names = [d[0].upper() for d in cur.description]
    rows = [["" if v is None else str(v) for v in r] for r in cur.fetchall()]
    w = [max(len(n), *(len(r[i]) for r in rows)) for i, n in enumerate(names)]
    print("  ".join(n.ljust(w[i]) for i, n in enumerate(names)))
    print("  ".join("-" * x for x in w))
    for r in rows: print("  ".join(c.ljust(w[i]) for i, c in enumerate(r)))
    print("(%d rows)\n" % len(rows))
show("SELECT * FROM dept")
show("SELECT deptno, COUNT(*) AS staff, SUM(sal) AS payroll, ROUND(AVG(sal),2) AS avg_sal FROM emp GROUP BY deptno ORDER BY deptno")
show("SELECT job, COUNT(*) AS n, MIN(sal) AS lowest, MAX(sal) AS highest FROM emp GROUP BY job ORDER BY job")
```
```output
DEPTNO  DNAME       LOC     
------  ----------  --------
10      ACCOUNTING  NEW YORK
20      RESEARCH    DALLAS  
30      SALES       CHICAGO 
40      OPERATIONS  BOSTON  
(4 rows)

DEPTNO  STAFF  PAYROLL  AVG_SAL
------  -----  -------  -------
10      3      8750     2916.67
20      5      10875    2175.0 
30      6      9400     1566.67
(3 rows)

JOB        N  LOWEST  HIGHEST
---------  -  ------  -------
ANALYST    2  3000    3000   
CLERK      4  800     1300   
MANAGER    3  2450    2975   
PRESIDENT  1  5000    5000   
SALESMAN   4  1250    1600   
(5 rows)
```
Keep these totals in mind; they are used to check the PL/SQL results later: 14 employees, payroll 29,025, department 10 pays 8,750, department 20 pays 10,875 and department 30 pays 9,400.

## 1.7 Fundamental SQL: DDL

SQL commands fall into families. **DDL** (Data Definition Language) creates and changes objects: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`. DDL **commits** automatically, before and after it runs, so it cannot be rolled back.

**Oracle data types you will use**

| Type | Holds | Example |
|---|---|---|
| `VARCHAR2(n)` | Variable text up to *n* bytes (max 4000) | `'SMITH'` |
| `CHAR(n)` | Fixed-length text, padded with spaces | `'A'` |
| `NUMBER(p,s)` | Number with *p* digits, *s* after the point | `NUMBER(7,2)` holds 12345.67 |
| `DATE` | Date and time to the second | `DATE '2025-04-01'` |
| `TIMESTAMP` | Date and time with fractions of a second | `SYSTIMESTAMP` |
| `CLOB` / `BLOB` | Large text / binary data | a document, an image |

```sqlplus
CREATE TABLE student (
  roll_no   NUMBER(4)      CONSTRAINT pk_student PRIMARY KEY,
  name      VARCHAR2(30)   NOT NULL,
  program   VARCHAR2(10)   DEFAULT 'BCA',
  fee       NUMBER(8,2)    CONSTRAINT ck_fee CHECK (fee >= 0),
  email     VARCHAR2(50)   CONSTRAINT uq_email UNIQUE,
  dept_no   NUMBER(2)      CONSTRAINT fk_dept REFERENCES dept(deptno)
);

ALTER TABLE student ADD (joined DATE);
ALTER TABLE student MODIFY (name VARCHAR2(50));
ALTER TABLE student DROP COLUMN program;
ALTER TABLE student RENAME TO students;
TRUNCATE TABLE students;       -- removes all rows, keeps the table, cannot be rolled back
DROP TABLE students PURGE;     -- removes the table and bypasses the recycle bin
```

Oracle-specific objects used throughout the later units:

```sqlplus
CREATE SEQUENCE seq_empno START WITH 8000 INCREMENT BY 1 NOCACHE;
INSERT INTO emp (empno, ename, job, sal, deptno)
VALUES (seq_empno.NEXTVAL, 'GURUNG', 'CLERK', 900, 10);
SELECT seq_empno.CURRVAL FROM dual;       -- 8000

CREATE VIEW v_dept_pay AS
  SELECT deptno, SUM(sal) AS payroll FROM emp GROUP BY deptno;

CREATE INDEX idx_emp_job ON emp(job);
CREATE SYNONYM employees FOR scott.emp;
```

`DUAL` is a one-row, one-column table that exists so that you can evaluate an expression with SELECT, for instance `SELECT SYSDATE FROM dual;`. A **sequence** produces unique numbers (the Oracle replacement for AUTO_INCREMENT) and is the usual source of primary keys in triggers (Unit 5).

## 1.8 Fundamental SQL: DML and transaction control

**DML** changes data: `INSERT`, `UPDATE`, `DELETE`, `MERGE`. Changes are visible only to your session until you `COMMIT`.

```sqlplus
INSERT INTO dept VALUES (50, 'TRAINING', 'POKHARA');
UPDATE emp SET sal = sal * 1.10 WHERE deptno = 20;
DELETE FROM emp WHERE empno = 7369;

MERGE INTO emp_target t
USING emp_source s ON (t.empno = s.empno)
WHEN MATCHED THEN UPDATE SET t.sal = s.sal
WHEN NOT MATCHED THEN INSERT (empno, ename, sal) VALUES (s.empno, s.ename, s.sal);
```

`MERGE` ("upsert") updates matching rows and inserts the rest in one statement. **Transaction control** (TCL) groups statements into a unit of work:

| Command | Effect |
|---|---|
| `COMMIT` | Makes all changes of the transaction permanent and visible to others |
| `ROLLBACK` | Undoes all changes since the last commit |
| `SAVEPOINT name` | Marks a point inside the transaction |
| `ROLLBACK TO name` | Undoes only the changes after that savepoint |

```sqlplus
SQL> UPDATE emp SET sal = sal + 500 WHERE empno = 7369;
1 row updated.
SQL> SAVEPOINT after_smith;
Savepoint created.
SQL> UPDATE emp SET sal = 0 WHERE deptno = 10;
3 rows updated.
SQL> ROLLBACK TO after_smith;
Rollback complete.
SQL> SELECT sal FROM emp WHERE empno = 7369;

       SAL
----------
      1300
SQL> COMMIT;
Commit complete.
```

SMITH's pay was 800, so after the first update it is 1300; the rollback to the savepoint undoes only the zeroing of department 10. A transaction ends at COMMIT, ROLLBACK, any DDL statement, or a normal exit from SQL*Plus (which commits). Unit 2 shows the same commands inside PL/SQL.

## 1.9 Fundamental SQL: DCL

**DCL** (Data Control Language) controls who may do what: `GRANT` and `REVOKE`.

```sqlplus
CREATE USER ram IDENTIFIED BY "Ch0ose-Another";
GRANT CREATE SESSION TO ram;
GRANT SELECT, UPDATE (sal) ON emp TO ram;
GRANT EXECUTE ON raise_salary TO ram;      -- a stored procedure (Unit 6)
CREATE ROLE clerk_role;
GRANT SELECT ON emp TO clerk_role;
GRANT clerk_role TO ram;
REVOKE UPDATE ON emp FROM ram;
```

A **system privilege** (`CREATE TABLE`, `CREATE SESSION`) permits an action in the database; an **object privilege** (`SELECT ON emp`) permits an action on one object; a **role** bundles privileges. Stored programs make DCL powerful: you can grant `EXECUTE` on a procedure that updates a table without granting any right on the table itself, so users can change data only through approved logic.

## 1.10 Joins

A **join** combines rows of two or more tables. The queries below were run on the sample data; the table outputs are real.

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE dept (deptno INTEGER PRIMARY KEY, dname TEXT, loc TEXT);
INSERT INTO dept VALUES (10,'ACCOUNTING','NEW YORK'),(20,'RESEARCH','DALLAS'),(30,'SALES','CHICAGO'),(40,'OPERATIONS','BOSTON');
CREATE TABLE emp (empno INTEGER PRIMARY KEY, ename TEXT, mgr INTEGER, sal INTEGER, deptno INTEGER);
INSERT INTO emp VALUES (7369,'SMITH',7902,800,20),(7499,'ALLEN',7698,1600,30),(7521,'WARD',7698,1250,30),(7566,'JONES',7839,2975,20),
(7654,'MARTIN',7698,1250,30),(7698,'BLAKE',7839,2850,30),(7782,'CLARK',7839,2450,10),(7788,'SCOTT',7566,3000,20),(7839,'KING',NULL,5000,10),
(7844,'TURNER',7698,1500,30),(7876,'ADAMS',7788,1100,20),(7900,'JAMES',7698,950,30),(7902,'FORD',7566,3000,20),(7934,'MILLER',7782,1300,10);
""")
def show(title, sql):
    print("--", title)
    for r in db.execute(sql): print("  ", r)
show("equi-join (INNER)", "SELECT e.ename, d.dname FROM emp e JOIN dept d ON e.deptno = d.deptno WHERE e.sal > 2900 ORDER BY 1")
show("self-join: employee and manager", "SELECT e.ename, m.ename FROM emp e JOIN emp m ON e.mgr = m.empno WHERE e.deptno = 20 ORDER BY 1")
show("left outer: every department appears, even one with no employee", "SELECT d.dname, COUNT(e.empno) FROM dept d LEFT JOIN emp e ON e.deptno = d.deptno GROUP BY d.dname ORDER BY 1")
show("cross join size", "SELECT COUNT(*) FROM emp CROSS JOIN dept")
```
```output
-- equi-join (INNER)
   ('FORD', 'RESEARCH')
   ('JONES', 'RESEARCH')
   ('KING', 'ACCOUNTING')
   ('SCOTT', 'RESEARCH')
-- self-join: employee and manager
   ('ADAMS', 'SCOTT')
   ('FORD', 'JONES')
   ('JONES', 'KING')
   ('SCOTT', 'JONES')
   ('SMITH', 'FORD')
-- left outer: every department appears, even one with no employee
   ('ACCOUNTING', 3)
   ('OPERATIONS', 0)
   ('RESEARCH', 5)
   ('SALES', 6)
-- cross join size
   (56,)
```
The Oracle forms differ slightly. Oracle accepts both the ANSI form above and its older **comma form** with the join condition in WHERE; for outer joins the old form uses the `(+)` marker on the side that may lack rows:

```sqlplus
-- Oracle comma style
SELECT e.ename, d.dname FROM emp e, dept d WHERE e.deptno = d.deptno;
-- non-equi join with a salary-grade table
SELECT e.ename, g.grade FROM emp e, salgrade g WHERE e.sal BETWEEN g.losal AND g.hisal;
-- old outer join: DEPT rows are kept even if no EMP matches
SELECT d.dname, e.ename FROM dept d, emp e WHERE d.deptno = e.deptno(+);
-- ANSI full outer join (Oracle 9i and later)
SELECT d.dname, e.ename FROM dept d FULL OUTER JOIN emp e ON d.deptno = e.deptno;
```

::: caution Common mistake
Forgetting the join condition gives a **Cartesian product**: 14 employees times 4 departments is 56 rows, all combinations. Always count your conditions: joining *n* tables needs at least *n* - 1 join conditions.
:::

## 1.11 Subqueries

A **subquery** is a SELECT inside another statement. A **single-row** subquery returns one value and is used with `=`, `>`, `<`. A **multiple-row** subquery returns a list and is used with `IN`, `ANY`, `ALL`. A **correlated** subquery refers to a column of the outer query and is re-evaluated for each outer row. `EXISTS` tests whether a subquery returns any row.

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE emp (empno INTEGER PRIMARY KEY, ename TEXT, job TEXT, sal INTEGER, deptno INTEGER);
INSERT INTO emp VALUES (7369,'SMITH','CLERK',800,20),(7499,'ALLEN','SALESMAN',1600,30),(7521,'WARD','SALESMAN',1250,30),
(7566,'JONES','MANAGER',2975,20),(7654,'MARTIN','SALESMAN',1250,30),(7698,'BLAKE','MANAGER',2850,30),(7782,'CLARK','MANAGER',2450,10),
(7788,'SCOTT','ANALYST',3000,20),(7839,'KING','PRESIDENT',5000,10),(7844,'TURNER','SALESMAN',1500,30),(7876,'ADAMS','CLERK',1100,20),
(7900,'JAMES','CLERK',950,30),(7902,'FORD','ANALYST',3000,20),(7934,'MILLER','CLERK',1300,10);
""")
def show(title, sql):
    print("--", title); print("  ", [r[0] for r in db.execute(sql)])
show("above the company average (2073.21)", "SELECT ename FROM emp WHERE sal > (SELECT AVG(sal) FROM emp) ORDER BY ename")
show("earn the same as the best-paid clerk or more", "SELECT ename FROM emp WHERE sal >= (SELECT MAX(sal) FROM emp WHERE job='CLERK') AND job <> 'CLERK' ORDER BY ename")
show("correlated: above the average of own department", "SELECT ename FROM emp e WHERE sal > (SELECT AVG(sal) FROM emp WHERE deptno = e.deptno) ORDER BY ename")
show("IN: works in a department that has a manager earning over 2900", "SELECT ename FROM emp WHERE deptno IN (SELECT deptno FROM emp WHERE job='MANAGER' AND sal > 2900) ORDER BY ename")
show("NOT EXISTS: jobs held by exactly one employee", "SELECT DISTINCT job FROM emp e WHERE NOT EXISTS (SELECT 1 FROM emp x WHERE x.job = e.job AND x.empno <> e.empno)")
print("average:", round(db.execute("SELECT AVG(sal) FROM emp").fetchone()[0], 2))
```
```output
-- above the company average (2073.21)
   ['BLAKE', 'CLARK', 'FORD', 'JONES', 'KING', 'SCOTT']
-- earn the same as the best-paid clerk or more
   ['ALLEN', 'BLAKE', 'CLARK', 'FORD', 'JONES', 'KING', 'SCOTT', 'TURNER']
-- correlated: above the average of own department
   ['ALLEN', 'BLAKE', 'FORD', 'JONES', 'KING', 'SCOTT']
-- IN: works in a department that has a manager earning over 2900
   ['ADAMS', 'FORD', 'JONES', 'SCOTT', 'SMITH']
-- NOT EXISTS: jobs held by exactly one employee
   ['PRESIDENT']
average: 2073.21
```
In Oracle the same queries work unchanged; the set operators are `UNION`, `UNION ALL`, `INTERSECT` and `MINUS` (called `EXCEPT` in the standard and in most other systems). Oracle also adds **single-row functions** that PL/SQL uses constantly:

| Function | Result | Example |
|---|---|---|
| `NVL(x, y)` | *y* if *x* is NULL | `NVL(comm, 0)` turns a missing commission into 0 |
| `DECODE(x, a, r1, b, r2, d)` | IF-THEN-ELSE on equality | `DECODE(deptno, 10, 'ACC', 20, 'RES', 'OTHER')` |
| `UPPER`, `LOWER`, `INITCAP` | Case change | `INITCAP('rAM')` gives `Ram` |
| `SUBSTR(s, start, len)`, `INSTR`, `LENGTH` | Text pieces | `SUBSTR('KATHMANDU', 1, 4)` gives `KATH` |
| `ROUND(n, d)`, `TRUNC`, `MOD` | Numbers | `MOD(10, 3)` gives 1 |
| `SYSDATE`, `ADD_MONTHS`, `MONTHS_BETWEEN`, `TO_CHAR(d, 'DD-MON-YYYY')` | Dates | `ADD_MONTHS(SYSDATE, 6)` |
| `TO_NUMBER`, `TO_DATE` | Conversions | `TO_DATE('2025-04-01', 'YYYY-MM-DD')` |

## 1.12 Summary and exercises

An Oracle **instance** (SGA plus background processes) works on a **database** (data, redo and control files); commits are made durable by LGWR writing redo before DBWn writes data blocks. SQL*Plus runs SQL, PL/SQL and its own commands; the buffer commands LIST, APPEND, CHANGE, INPUT, DEL and CLEAR BUFFER edit the last statement, script files run with `@`, and `&` or `ACCEPT` bring values in at runtime. DDL (CREATE, ALTER, DROP, TRUNCATE) auto-commits, DML (INSERT, UPDATE, DELETE, MERGE) waits for COMMIT or ROLLBACK, DCL (GRANT, REVOKE) controls access. Joins and subqueries combine tables; correlated subqueries run once per outer row.

1. Distinguish the Oracle instance from the Oracle database. Name two memory structures and four background processes.
2. Explain why a committed change is safe even if the data block has not yet been written to the data file.
3. Describe the logical storage hierarchy from tablespace to block.
4. List the SQL*Plus buffer commands with the use of each, and show a short session that fixes a wrong department number in a query.
5. What is the difference between `&dno` and `&&dno`? Why must a text value be written as `'&job'`?
6. How do you save, run and spool a script? Write a script that reports the employees of a department entered by the user.
7. Classify these as DDL, DML, DCL or TCL: `TRUNCATE`, `MERGE`, `GRANT`, `SAVEPOINT`, `ALTER TABLE`, `DELETE`.
8. Why can `TRUNCATE TABLE emp` not be rolled back but `DELETE FROM emp` can?
9. Write queries on EMP and DEPT: (a) the name and department name of every employee earning over 2500; (b) employees who earn more than their own manager; (c) departments that have no employee; (d) the second highest salary.
10. Write a query that lists employees earning more than the average of their department, and explain why it is a correlated subquery.
11. A transaction updates 3 rows, creates a savepoint, updates 2 more, and rolls back to the savepoint. How many rows stay changed? What happens if a `CREATE TABLE` is then executed?
12. How many rows does `SELECT * FROM emp, dept;` return for the sample data, and why?

**Answers to the numerical and query items.** (11) 3 rows stay changed (until the transaction ends); the `CREATE TABLE` commits them. (12) $14\times4=56$ rows. (9a) `SELECT e.ename, d.dname FROM emp e JOIN dept d ON e.deptno = d.deptno WHERE e.sal > 2500;` gives JONES, BLAKE, SCOTT, KING, FORD (5 rows). (9b) `SELECT e.ename FROM emp e JOIN emp m ON e.mgr = m.empno WHERE e.sal > m.sal;` gives SCOTT and FORD, each earning 3000 against JONES at 2975. (9c) `SELECT dname FROM dept d WHERE NOT EXISTS (SELECT 1 FROM emp e WHERE e.deptno = d.deptno);` gives OPERATIONS. (9d) `SELECT MAX(sal) FROM emp WHERE sal < (SELECT MAX(sal) FROM emp);` gives 3000.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the Oracle instance and database.**

The database is the set of files that store data permanently: data files, redo log files and control files. The instance is the SGA plus the background processes that run on the server. The SGA holds the database buffer cache (copies of data blocks), the shared pool (parsed SQL and PL/SQL) and the redo log buffer. Background processes include DBWn (writes dirty blocks), LGWR (writes redo at commit), CKPT, SMON (instance recovery) and PMON (cleans up failed sessions). Users connect to the instance, which reads and writes the database files on their behalf.

**Q2 (5 marks). Explain the SQL*Plus buffer commands with an example.**

SQL*Plus keeps the last SQL statement or PL/SQL block in the SQL buffer. `LIST` shows it with line numbers, `LIST n` selects line *n*, `CHANGE /old/new/` replaces text in the current line, `APPEND text` adds text at its end, `INPUT text` inserts a line after it, `DEL` removes it and `CLEAR BUFFER` empties the buffer; `/` or `RUN` executes the buffer. Example: after `SELECT ename FROM emp WHERE deptno = 10;`, the commands `CHANGE /10/20/` and `/` rerun the query for department 20 without retyping.

**Q3 (10 marks). Describe the Oracle database architecture.**

*Introduction.* An Oracle server is an instance working on a database, and the logical and physical structures are kept separate.

*Memory.* The SGA is shared and contains the database buffer cache, shared pool and redo log buffer; each server process also has a private PGA for sorting and session data.

*Processes.* DBWn writes changed blocks to the data files, LGWR writes redo to the log files at commit, CKPT records checkpoints, SMON recovers the instance after a crash, PMON cleans up after dead sessions, and ARCn archives the redo logs.

*Files.* Data files hold tables and indexes, redo log files hold the history of changes, and control files record the physical structure.

*Logical storage.* Tablespaces contain segments, segments consist of extents and extents of data blocks; a schema is the set of objects owned by a user and the data dictionary describes all of them.

*Example and conclusion.* In an UPDATE the server process reads the block into the buffer cache, writes redo and undo, changes the block, and LGWR makes the change durable at COMMIT. The separation of fast memory and durable files gives Oracle both speed and recoverability.
