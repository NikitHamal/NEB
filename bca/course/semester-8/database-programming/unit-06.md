---
subject: Database Programming
grade: BCA Semester 8 (Elective III)
unit: 6
title: Records and Procedures
hours: 5
area: BCA 453 · Database Programming · Unit 6
---

Until now every program was an anonymous block that had to be pasted again and again. A real system needs reusable pieces: "raise this employee's salary", "hire a person", "report this department". Those are **stored procedures**, named blocks kept inside the database, compiled once and called by every program. To pass a whole row to them conveniently, PL/SQL also gives us the **record**, a variable that holds several related fields.

::: key What this unit gives you
- Records: `%ROWTYPE`, user-defined record types, and records inside records (nested records).
- Procedures: block structure, creating, calling, replacing and dropping them.
- Parameters: IN, OUT and IN OUT, positional and named notation, default values.
- Complete worked procedures for raising salaries, hiring staff and summarising a department.
:::

## 6.1 Records

A **record** is a composite variable made of **fields** of different types, treated as one unit, like a row or a C `struct`. Fields are reached with dot notation: `record_name.field_name`.

**Record type 1: `%ROWTYPE`.** One field for each column of a table, view or cursor, with the same names and types (met in Units 2 and 4).

**Record type 2: user-defined.** Declare a type with the fields you want, then variables of it.

```plsql
TYPE type_name IS RECORD (
  field1  datatype [NOT NULL] [:= default],
  field2  datatype,
  ... );
```

```plsql
DECLARE
  TYPE t_emp_rec IS RECORD (
    name    emp.ename%TYPE,
    job     emp.job%TYPE,
    pay     emp.sal%TYPE,
    dept    emp.deptno%TYPE := 10          -- a default for the field
  );
  r  t_emp_rec;
BEGIN
  SELECT ename, job, sal, deptno INTO r.name, r.job, r.pay, r.dept
  FROM   emp WHERE empno = 7788;
  DBMS_OUTPUT.PUT_LINE(r.name || ' (' || r.job || ') earns ' || r.pay || ' in department ' || r.dept);
END;
/
```
```output
SCOTT (ANALYST) earns 3000 in department 20

PL/SQL procedure successfully completed.
```

The SELECT could also write `INTO r` if the columns in the SELECT list matched the fields in number, order and type. Rules for working with records:

| Operation | Allowed? | Example |
|---|---|---|
| Assign one record to another of the **same type** | Yes | `r2 := r1;` |
| Assign a `%ROWTYPE` record to a variable of a *different* type with the same fields | No | copy the fields one by one |
| Compare two records with `=` | **No** | compare the fields: `r1.pay = r2.pay` |
| Fetch a row into a record | Yes | `SELECT * INTO v_emp ...`, `FETCH c INTO r` |
| Insert a whole record | Yes | `INSERT INTO emp VALUES v_emp;` |
| Update a row from a record | Yes | `UPDATE emp SET ROW = v_emp WHERE empno = v_emp.empno;` |
| Record as procedure parameter or function result | Yes | Section 6.5 |

```plsql
DECLARE
  v_emp  emp%ROWTYPE;
BEGIN
  v_emp.empno    := 8200;
  v_emp.ename    := 'THAPA';
  v_emp.job      := 'CLERK';
  v_emp.sal      := 950;
  v_emp.deptno   := 10;
  INSERT INTO emp VALUES v_emp;                   -- one statement, no column list
  DBMS_OUTPUT.PUT_LINE('Inserted ' || v_emp.ename || ', rows: ' || SQL%ROWCOUNT);
  v_emp.sal := v_emp.sal + 100;
  UPDATE emp SET ROW = v_emp WHERE empno = v_emp.empno;
  DBMS_OUTPUT.PUT_LINE('Updated salary to ' || v_emp.sal);
  ROLLBACK;
END;
/
```
```output
Inserted THAPA, rows: 1
Updated salary to 1050

PL/SQL procedure successfully completed.
```

The fields not set (`mgr`, `hiredate`, `comm`) stay NULL. Records are the natural way to carry a row between a cursor, a procedure and a function without a long list of variables.

## 6.2 Nested records

A field of a record may itself be a record. This models structured data such as a person with an address.

```plsql
DECLARE
  TYPE t_address IS RECORD (
    town     VARCHAR2(20),
    district VARCHAR2(20)
  );
  TYPE t_person IS RECORD (
    name     VARCHAR2(30),
    age      NUMBER(3),
    address  t_address                       -- a record inside a record
  );
  p  t_person;
BEGIN
  p.name := 'Sita Rai';
  p.age  := 24;
  p.address.town     := 'Pokhara';
  p.address.district := 'Kaski';
  DBMS_OUTPUT.PUT_LINE(p.name || ' (' || p.age || ') lives in ' ||
                       p.address.town || ', ' || p.address.district);
END;
/
```
```output
Sita Rai (24) lives in Pokhara, Kaski

PL/SQL procedure successfully completed.
```

The inner type must be declared **before** the outer type that uses it. The whole inner record can be copied with one assignment, `p.address := other_address;`, and the whole person with `p2 := p;`. A `%ROWTYPE` record cannot contain a nested record, but a user-defined type can have a field declared as `emp%ROWTYPE`:

```plsql
TYPE t_entry IS RECORD (emp_row emp%ROWTYPE, dept_row dept%ROWTYPE);
```

With such a type, `e.emp_row.ename` and `e.dept_row.dname` hold an employee and the department in a single variable.

## 6.3 Procedures

A **procedure** is a named block that performs an action and may return values through its parameters. It is compiled and **stored in the database**; Oracle keeps its parsed form in the shared pool for all sessions.

```plsql
CREATE [OR REPLACE] PROCEDURE procedure_name
  [(parameter1 [IN | OUT | IN OUT] datatype [:= default], ...)]
  [AUTHID {DEFINER | CURRENT_USER}]
IS | AS
  -- declarations (no DECLARE keyword here)
BEGIN
  -- executable statements
[EXCEPTION
  -- handlers]
END [procedure_name];
/
```

Differences from an anonymous block: it begins with a header instead of `DECLARE`, it has a name, it is stored and compiled once, it takes parameters, and it can be granted to other users. A procedure is **called as a statement**; a function (Unit 7) is called inside an expression.

```plsql
CREATE OR REPLACE PROCEDURE raise_salary (
  p_empno  IN emp.empno%TYPE,
  p_pct    IN NUMBER DEFAULT 10                  -- percentage; 10 if the caller says nothing
) IS
  v_name  emp.ename%TYPE;
  v_old   emp.sal%TYPE;
  v_new   emp.sal%TYPE;
BEGIN
  SELECT ename, sal INTO v_name, v_old FROM emp WHERE empno = p_empno;
  v_new := v_old * (1 + p_pct / 100);
  UPDATE emp SET sal = v_new WHERE empno = p_empno;
  DBMS_OUTPUT.PUT_LINE(v_name || ': ' || v_old || ' -> ' || v_new);
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RAISE_APPLICATION_ERROR(-20003, 'Employee ' || p_empno || ' not found');
END raise_salary;
/
```

```plsql
SQL> EXECUTE raise_salary(7369, 25)
SMITH: 800 -> 1000

PL/SQL procedure successfully completed.

SQL> BEGIN raise_salary(7499); END;          -- from PL/SQL: default of 10 percent
  2  /
ALLEN: 1600 -> 1760

SQL> EXEC raise_salary(9999)
BEGIN raise_salary(9999); END;
*
ERROR at line 1:
ORA-20003: Employee 9999 not found
ORA-06512: at "SCOTT.RAISE_SALARY", line 15
ORA-06512: at line 1
```

SMITH's pay of 800 rises by 25 percent to 1000, and ALLEN's 1600 by the default 10 percent to 1760. `EXECUTE` (short `EXEC`) is a SQL*Plus command that wraps the call in `BEGIN ... END;`. The procedure does not commit; the caller decides.

**Managing procedures**

| Task | How |
|---|---|
| Compile errors | `Warning: Procedure created with compilation errors.` then `SHOW ERRORS` |
| Source | `SELECT text FROM user_source WHERE name = 'RAISE_SALARY' ORDER BY line;` |
| List | `SELECT object_name, status FROM user_objects WHERE object_type = 'PROCEDURE';` |
| Remove | `DROP PROCEDURE raise_salary;` |
| Allow others | `GRANT EXECUTE ON raise_salary TO ram;` |
| Dependencies | `USER_DEPENDENCIES`; changing a table marks dependent procedures `INVALID`, and Oracle recompiles them on the next call (or `ALTER PROCEDURE raise_salary COMPILE;`) |

With the default `AUTHID DEFINER` a procedure runs with the **owner's** rights, so a user with only `EXECUTE` can change EMP through the procedure without any privilege on EMP. With `AUTHID CURRENT_USER` it runs with the caller's own rights.

## 6.4 Parameters: IN, OUT and IN OUT

Parameters carry data into and out of a procedure. Those in the header are **formal** parameters; the values in a call are **actual** parameters. Formal parameters are given a type but **no size** (`p_name VARCHAR2`, not `VARCHAR2(30)`); the size comes from the actual value.

| Mode | Direction | Inside the procedure | Actual parameter may be | Default if omitted |
|---|---|---|---|---|
| `IN` (the default) | Caller to procedure | Read-only, like a constant | A literal, expression or variable | A `DEFAULT` value can be declared |
| `OUT` | Procedure to caller | Starts as NULL; must be assigned | A **variable** only | Must be given |
| `IN OUT` | Both ways | Read and write | A **variable** only | Must be given |

```svgfig label="6.1" caption="Parameter modes. IN sends a value to the procedure, OUT returns one, IN OUT does both."
f = Fig(640, 190)
f.box(10, 20, 170, 150, "Calling\nprogram", fill=SOFT, stroke=SLATE, size=11)
f.box(460, 20, 170, 150, "Procedure", fill=BLUE, stroke=NAVY, size=11)
f.arrow([(180, 50), (460, 50)], color=NAVY, label="IN: p_empno = 7369", lpos=(320, 40))
f.arrow([(460, 100), (180, 100)], color=TEAL, label="OUT: p_name, p_sal", lpos=(320, 90))
f.arrow([(180, 150), (460, 150)], color=AMBER, both=True, label="IN OUT: p_total", lpos=(320, 140))
```

**Example: IN and OUT.** The procedure returns a name and a salary through OUT parameters.

```plsql
CREATE OR REPLACE PROCEDURE get_emp (
  p_empno IN  emp.empno%TYPE,
  p_name  OUT emp.ename%TYPE,
  p_sal   OUT emp.sal%TYPE
) IS
BEGIN
  SELECT ename, sal INTO p_name, p_sal FROM emp WHERE empno = p_empno;
END;
/
```

```plsql
SQL> VARIABLE b_name VARCHAR2(10)
SQL> VARIABLE b_sal  NUMBER
SQL> EXEC get_emp(7839, :b_name, :b_sal)
PL/SQL procedure successfully completed.
SQL> PRINT b_name b_sal

B_NAME
--------------------------------
KING

     B_SAL
----------
      5000
```

In a PL/SQL block the actual OUT parameters are ordinary variables: `get_emp(7839, v_name, v_sal);`. A call with a literal for an OUT parameter (`get_emp(7839, 'KING', 5000)`) is a compile error (PLS-00363).

**Example: IN OUT.** A swap needs values to go in and come out.

```plsql
CREATE OR REPLACE PROCEDURE swap (p_a IN OUT NUMBER, p_b IN OUT NUMBER) IS
  v_tmp NUMBER;
BEGIN
  v_tmp := p_a;  p_a := p_b;  p_b := v_tmp;
END;
/

DECLARE
  x NUMBER := 5;  y NUMBER := 9;
BEGIN
  swap(x, y);
  DBMS_OUTPUT.PUT_LINE('x = ' || x || ', y = ' || y);
END;
/
```
```output
x = 9, y = 5

PL/SQL procedure successfully completed.
```

**Passing the actual parameters.** Three notations:

| Notation | Example | Rules |
|---|---|---|
| **Positional** | `raise_salary(7499, 5)` | Order must match the header |
| **Named** | `raise_salary(p_pct => 5, p_empno => 7499)` | Any order; skip defaulted parameters |
| **Mixed** | `raise_salary(7499, p_pct => 5)` | Positional ones first, then named |

Named notation makes calls readable and survives the addition of new defaulted parameters. After `raise_salary(p_pct => 5, p_empno => 7499)`, ALLEN's 1600 becomes 1680 (an increase of 5 percent).

**Example: several OUT values.**

```plsql
CREATE OR REPLACE PROCEDURE dept_stats (
  p_dno    IN  dept.deptno%TYPE,
  p_count  OUT NUMBER,
  p_total  OUT NUMBER,
  p_avg    OUT NUMBER
) IS
BEGIN
  SELECT COUNT(*), NVL(SUM(sal), 0) INTO p_count, p_total FROM emp WHERE deptno = p_dno;
  p_avg := CASE WHEN p_count = 0 THEN 0 ELSE ROUND(p_total / p_count, 2) END;   -- avoid dividing by 0
END dept_stats;
/

DECLARE
  n NUMBER;  t NUMBER;  a NUMBER;
BEGIN
  FOR d IN (SELECT deptno FROM dept ORDER BY deptno) LOOP
    dept_stats(d.deptno, n, t, a);
    DBMS_OUTPUT.PUT_LINE('Department ' || d.deptno || ': ' || n || ' employees, payroll ' || t || ', average ' || a);
  END LOOP;
END;
/
```
```output
Department 10: 3 employees, payroll 8750, average 2916.67
Department 20: 5 employees, payroll 10875, average 2175
Department 30: 6 employees, payroll 9400, average 1566.67
Department 40: 0 employees, payroll 0, average 0

PL/SQL procedure successfully completed.
```

The guard in `p_avg` matters: for department 40 an unguarded division would raise `ZERO_DIVIDE`. Two further points on parameters. First, an OUT or IN OUT value is normally copied back to the caller only if the procedure ends **normally**; with an unhandled exception the caller's variable keeps its old value (the `NOCOPY` hint changes this and is for large collections). Second, a parameter may be a record, so a whole row travels as one argument.

## 6.5 A larger procedure: hiring with checks, and a record parameter

Real procedures validate input, use sequences and exceptions, and leave the commit to the caller:

```plsql
CREATE OR REPLACE PROCEDURE hire_employee (
  p_name   IN  emp.ename%TYPE,
  p_job    IN  emp.job%TYPE,
  p_sal    IN  emp.sal%TYPE,
  p_dno    IN  emp.deptno%TYPE,
  p_empno  OUT emp.empno%TYPE
) IS
  v_dummy  dept.deptno%TYPE;
BEGIN
  IF p_sal <= 0 THEN
    RAISE_APPLICATION_ERROR(-20004, 'Salary must be positive');
  END IF;
  SELECT deptno INTO v_dummy FROM dept WHERE deptno = p_dno;    -- does the department exist?
  INSERT INTO emp (empno, ename, job, sal, hiredate, deptno)
  VALUES (seq_empno.NEXTVAL, UPPER(p_name), p_job, p_sal, SYSDATE, p_dno)
  RETURNING empno INTO p_empno;
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RAISE_APPLICATION_ERROR(-20005, 'Department ' || p_dno || ' does not exist');
END hire_employee;
/

-- a procedure can also take a whole row: PROCEDURE show_emp (p_row IN emp%ROWTYPE) IS ...
```

```plsql
DECLARE
  v_id emp.empno%TYPE;
BEGIN
  hire_employee('Gurung', 'CLERK', 900, 10, v_id);
  DBMS_OUTPUT.PUT_LINE('Hired GURUNG with empno ' || v_id);
END;
/
```
```output
Hired GURUNG with empno 8000

PL/SQL procedure successfully completed.
```

```plsql
SQL> DECLARE
  2    v_id emp.empno%TYPE;
  3  BEGIN
  4    hire_employee('Karki', 'CLERK', 900, 99, v_id);      -- there is no department 99
  5  END;
  6  /
DECLARE
*
ERROR at line 1:
ORA-20005: Department 99 does not exist
ORA-06512: at "SCOTT.HIRE_EMPLOYEE", line 19
ORA-06512: at line 4
```

The first block succeeds (the sequence starts at 8000) and the second call is rejected by the procedure, which is the point of storing the rule in one place: every application that hires through `hire_employee` obeys it. Procedures can call other procedures, and a procedure may be defined **inside** another block's declaration section as a *local* procedure that exists only while that block runs.

::: tip Exam tip
For "differentiate procedure and function" write: a procedure is called as a statement and returns values only through OUT or IN OUT parameters; a function is used inside an expression, must `RETURN` exactly one value, and can be called from SQL. Unit 7 covers functions.
:::

## 6.6 Summary and exercises

A record groups fields: `%ROWTYPE` copies a table or cursor row, `TYPE ... IS RECORD` defines your own fields, and records may nest. Whole records can be assigned, fetched, inserted and used in `UPDATE ... SET ROW`, but not compared with `=`. A stored procedure (`CREATE OR REPLACE PROCEDURE`) is a named, compiled block called as a statement. Parameters are IN (read-only), OUT (returned) or IN OUT; they are passed by position, by name (`=>`) or mixed, and may have defaults. The owner's rights apply by default, so procedures give controlled access to tables.

1. What is a record? Distinguish `%ROWTYPE` records from user-defined records.
2. Write a user-defined record type for (roll number, name, marks), fill it and print it.
3. Which operations on records are allowed, and which is not?
4. What is a nested record? Write an example with a person and an address.
5. What is a stored procedure? How does it differ from an anonymous block?
6. Write the syntax of CREATE PROCEDURE and explain each part. How is a procedure called from SQL*Plus and from a block?
7. Explain IN, OUT and IN OUT with an example each.
8. Explain positional, named and mixed notation with `raise_salary`. What is the use of a default value?
9. Write a procedure that takes a department number and prints the name of the best paid employee of that department.
10. Write a procedure `fire_employee(p_empno)` that deletes an employee and raises an error with `RAISE_APPLICATION_ERROR` if no row was deleted.
11. Why does a procedure usually not COMMIT? What does `AUTHID DEFINER` mean?
12. After `raise_salary(7369, 25)` what is SMITH's new salary? After `raise_salary(p_empno => 7499)`?
13. `swap(x, y)` is called with `x = 5` and `y = 9`. What are the values afterwards? What if the call is `swap(5, 9)`?

**Answers to the numerical items.** (12) 800 x 1.25 = 1000; 1600 x 1.10 = 1760. (13) `x = 9`, `y = 5`; the call `swap(5, 9)` does not compile, because actual parameters for IN OUT must be variables (PLS-00363). (9) The idea: `SELECT ename INTO v FROM emp WHERE deptno = p_dno AND sal = (SELECT MAX(sal) FROM emp WHERE deptno = p_dno)` with a `TOO_MANY_ROWS` handler for ties (department 20 has two employees at 3000).

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the parameter modes of a procedure.**

An IN parameter passes a value into the procedure and is read-only inside; it is the default and may be given a default value. An OUT parameter returns a value to the caller; it starts as NULL, must be assigned and needs a variable as the actual parameter. An IN OUT parameter passes a value in and returns a changed value; it also needs a variable. Example: `get_emp(p_empno IN, p_name OUT, p_sal OUT)` returns KING and 5000 for 7839, and `swap(p_a IN OUT, p_b IN OUT)` turns 5 and 9 into 9 and 5.

**Q2 (5 marks). What is a nested record? Give an example.**

A nested record is a record that has another record as a field. The inner type is declared first: `TYPE t_address IS RECORD (town VARCHAR2(20), district VARCHAR2(20));` then `TYPE t_person IS RECORD (name VARCHAR2(30), age NUMBER(3), address t_address);`. Fields are reached by repeated dot notation, `p.address.town := 'Pokhara';`. The whole inner record can be assigned at once. It models structured data without many separate variables.

**Q3 (10 marks). Explain stored procedures with syntax, creation, execution and parameters.**

*Introduction.* A stored procedure is a named PL/SQL block stored in the database and compiled once, which performs an action and may return values.

*Syntax.* `CREATE OR REPLACE PROCEDURE name (params) IS declarations BEGIN statements EXCEPTION handlers END;` with no DECLARE keyword.

*Parameters.* IN, OUT and IN OUT, passed by position, name or mixed, with optional defaults.

*Example.* `raise_salary(p_empno IN, p_pct IN DEFAULT 10)` reads the salary, updates it and prints the change; `EXECUTE raise_salary(7369, 25)` prints `SMITH: 800 -> 1000`, and an unknown number raises ORA-20003.

*Management.* `SHOW ERRORS`, `USER_SOURCE`, `DROP PROCEDURE`, `GRANT EXECUTE`; changing a table invalidates dependent procedures, which are recompiled on the next call.

*Advantages.* Reuse, one round trip, central business rules, security through EXECUTE and the owner's rights.

*Conclusion.* Procedures make database logic modular, shared and safe.

**Q4 (10 marks). Explain records in PL/SQL and write a procedure that uses a record.**

*Records.* A record is a composite variable of related fields. `%ROWTYPE` creates one with the columns of a table or cursor; `TYPE ... IS RECORD` defines custom fields, which may be records themselves.

*Operations.* Records can be assigned to records of the same type, filled by `SELECT INTO` and `FETCH`, inserted with `INSERT INTO t VALUES rec` and applied with `UPDATE t SET ROW = rec`; they cannot be compared with `=`.

*Procedure.* `PROCEDURE show_emp(p_row IN emp%ROWTYPE) IS BEGIN DBMS_OUTPUT.PUT_LINE(p_row.ename || ' ' || p_row.job || ' ' || p_row.sal); END;` receives a whole employee row as one parameter, which a caller fills with `SELECT * INTO v_emp FROM emp WHERE empno = 7839;` to print `KING PRESIDENT 5000`.

*Example of use.* `INSERT INTO emp VALUES v_emp;` adds a row from a record with no column list.

*Conclusion.* Records reduce long lists of variables and parameters to one meaningful unit and make code easier to maintain.
