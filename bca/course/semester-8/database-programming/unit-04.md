---
subject: Database Programming
grade: BCA Semester 8 (Elective III)
unit: 4
title: Database Cursors
hours: 5
area: BCA 453 · Database Programming · Unit 4
---

`SELECT INTO` works for one row. A report on every employee, a month-end raise for each clerk, a transfer of all pending orders: these need to look at **many rows, one at a time**, in a program. SQL returns a set; a procedural language processes one item per step. The **cursor** is the bridge between the two. Think of it as a bookmark that moves down the result of a query.

::: key What this unit gives you
- What a cursor and the context area are; implicit and explicit cursors and their attributes.
- The four steps DECLARE, OPEN, FETCH, CLOSE, and the three loop styles, including the cursor FOR loop.
- Parameterised cursors, nested cursors, and `FOR UPDATE` with `WHERE CURRENT OF`.
- A short look at REF cursors and `BULK COLLECT`.
:::

## 4.1 Types of cursors

When Oracle runs a SQL statement it uses a private memory area, the **context area** (in the PGA), that holds the statement's text, the rows it fetched and a pointer to the current row. A **cursor** is a name or handle for that area.

| Cursor | Who creates it | Used for |
|---|---|---|
| **Implicit** | Oracle, for every DML statement and every `SELECT ... INTO` | Single-row work; named `SQL`; attributes `SQL%FOUND`, `SQL%NOTFOUND`, `SQL%ROWCOUNT`, `SQL%ISOPEN` (always FALSE after the statement) |
| **Explicit** | You, with `CURSOR name IS SELECT ...` | A query that returns **several rows** that you process one by one |
| **Cursor variable** (REF CURSOR) | You, as a variable of a cursor type | Passing a result set between programs (Section 4.7) |

The implicit cursor was met in Unit 2. This unit is about the explicit cursor.

## 4.2 The explicit cursor: DECLARE, OPEN, FETCH, CLOSE

An explicit cursor is processed in four steps.

| Step | Statement | What happens |
|---|---|---|
| 1. **Declare** | `CURSOR c_emp IS SELECT ename, sal FROM emp WHERE deptno = 10 ORDER BY ename;` | Names the query; nothing runs yet |
| 2. **Open** | `OPEN c_emp;` | Oracle runs the query and fixes the result set; the pointer is before the first row |
| 3. **Fetch** | `FETCH c_emp INTO v_ename, v_sal;` | Copies the current row into variables and moves the pointer on |
| 4. **Close** | `CLOSE c_emp;` | Releases the context area |

**Cursor attributes** are written after the cursor name:

| Attribute | Value |
|---|---|
| `c%ISOPEN` | `TRUE` if the cursor is open |
| `c%FOUND` | `TRUE` if the last FETCH returned a row (NULL before the first fetch) |
| `c%NOTFOUND` | `TRUE` if the last FETCH did **not** return a row: the signal to leave the loop |
| `c%ROWCOUNT` | The number of rows fetched so far |

```plsql
DECLARE
  CURSOR c_emp IS
    SELECT ename, sal FROM emp WHERE deptno = 10 ORDER BY ename;
  v_ename emp.ename%TYPE;
  v_sal   emp.sal%TYPE;
BEGIN
  OPEN c_emp;
  LOOP
    FETCH c_emp INTO v_ename, v_sal;
    EXIT WHEN c_emp%NOTFOUND;                  -- test straight after the FETCH
    DBMS_OUTPUT.PUT_LINE(c_emp%ROWCOUNT || '. ' || v_ename || ' ' || v_sal);
  END LOOP;
  DBMS_OUTPUT.PUT_LINE('Rows fetched: ' || c_emp%ROWCOUNT);
  CLOSE c_emp;
END;
/
```
```output
1. CLARK 2450
2. KING 5000
3. MILLER 1300
Rows fetched: 3

PL/SQL procedure successfully completed.
```

Notice that `%NOTFOUND` is tested **immediately after** the FETCH and **before** the row is used. If the test comes later, the last row is processed twice or the loop runs once too often. Fetching into a record is shorter:

```plsql
DECLARE
  CURSOR c_dept IS SELECT * FROM dept ORDER BY deptno;
  r_dept c_dept%ROWTYPE;                      -- a record that matches the cursor's columns
BEGIN
  OPEN c_dept;
  FETCH c_dept INTO r_dept;
  DBMS_OUTPUT.PUT_LINE(r_dept.deptno || ' ' || r_dept.dname || ' ' || r_dept.loc);
  CLOSE c_dept;
END;
/
```
```output
10 ACCOUNTING NEW YORK

PL/SQL procedure successfully completed.
```

**Cursor errors.** Opening an open cursor raises `CURSOR_ALREADY_OPEN` (ORA-06511); fetching from or closing a cursor that is not open raises `INVALID_CURSOR` (ORA-01001). Fetching after the last row does **not** raise an error; it just sets `%NOTFOUND`. Always close a cursor, because open cursors per session are limited (`OPEN_CURSORS`, often 300) and exceeding it raises `ORA-01000: maximum open cursors exceeded`.

## 4.3 Cursor loops

There are three ways to loop over a cursor.

**1. Simple LOOP** (as above): `OPEN`, `LOOP`, `FETCH`, `EXIT WHEN c%NOTFOUND`, `END LOOP`, `CLOSE`.

**2. WHILE loop.** Fetch once **before** the loop, test `%FOUND`, and fetch again at the **end** of each pass:

```plsql
DECLARE
  CURSOR c_sal IS SELECT ename, sal FROM emp WHERE deptno = 30 ORDER BY sal DESC, ename;
  r c_sal%ROWTYPE;
  v_total NUMBER := 0;
BEGIN
  OPEN c_sal;
  FETCH c_sal INTO r;                           -- priming fetch
  WHILE c_sal%FOUND LOOP
    v_total := v_total + r.sal;
    FETCH c_sal INTO r;                         -- next row, at the end of the pass
  END LOOP;
  DBMS_OUTPUT.PUT_LINE('Rows: ' || c_sal%ROWCOUNT || ', payroll of department 30: ' || v_total);
  CLOSE c_sal;
END;
/
```
```output
Rows: 6, payroll of department 30: 9400

PL/SQL procedure successfully completed.
```

**3. The cursor FOR loop.** The shortest and the safest form: Oracle declares the record, **opens** the cursor, **fetches** each row and **closes** the cursor, even if an exception ends the loop. You write no OPEN, FETCH, CLOSE or `%NOTFOUND` test.

```plsql
DECLARE
  CURSOR c_sal IS SELECT ename, sal FROM emp WHERE deptno = 30 ORDER BY sal DESC, ename;
  v_top VARCHAR2(10);
BEGIN
  FOR r IN c_sal LOOP                                       -- r is declared implicitly
    IF c_sal%ROWCOUNT = 1 THEN v_top := r.ename; END IF;    -- the first row is the best paid
    DBMS_OUTPUT.PUT_LINE(RPAD(r.ename, 8) || LPAD(r.sal, 5));
  END LOOP;
  DBMS_OUTPUT.PUT_LINE('Best paid in department 30: ' || v_top);
END;
/
```
```output
BLAKE    2850
ALLEN    1600
TURNER   1500
MARTIN   1250
WARD     1250
JAMES     950
Best paid in department 30: BLAKE

PL/SQL procedure successfully completed.
```

(`c_sal%ROWCOUNT` is readable inside the loop but not after it, because the cursor is closed by then.) The query can also be written **inside** the loop without a declared cursor, which is the most compact form:

```plsql
BEGIN
  FOR r IN (SELECT job, COUNT(*) AS n, SUM(sal) AS pay FROM emp GROUP BY job ORDER BY job) LOOP
    DBMS_OUTPUT.PUT_LINE(RPAD(r.job, 10) || r.n || ' ' || r.pay);
  END LOOP;
END;
/
```
```output
ANALYST   2 6000
CLERK     4 4150
MANAGER   3 8275
PRESIDENT 1 5000
SALESMAN  4 5600

PL/SQL procedure successfully completed.
```

| Loop | OPEN/FETCH/CLOSE | Needs `%NOTFOUND` test | Record declared | Choose it when |
|---|---|---|---|---|
| Simple | By you | Yes | By you | You need full control of every step |
| WHILE | By you | `%FOUND` | By you | You want a priming fetch, e.g. to decide before processing |
| Cursor FOR | Automatic | No | Automatic | The usual case: process every row |

## 4.4 Parameterised cursors

A cursor may take **parameters**, so that the same cursor can be opened again with different values. Parameters are listed in the declaration, may have defaults, are read-only, and may be used only where a literal could be used in the query. Pass the values at `OPEN`, or in a FOR loop.

```plsql
DECLARE
  CURSOR c_pay (p_dno NUMBER, p_min NUMBER DEFAULT 0) IS
    SELECT ename, sal FROM emp
    WHERE  deptno = p_dno AND sal >= p_min
    ORDER  BY sal DESC, ename;
BEGIN
  DBMS_OUTPUT.PUT_LINE('Department 20, salary at least 2000:');
  FOR r IN c_pay(20, 2000) LOOP
    DBMS_OUTPUT.PUT_LINE('  ' || r.ename || ' ' || r.sal);
  END LOOP;
  DBMS_OUTPUT.PUT_LINE('Department 10, any salary:');
  FOR r IN c_pay(10) LOOP                          -- p_min takes its default, 0
    DBMS_OUTPUT.PUT_LINE('  ' || r.ename || ' ' || r.sal);
  END LOOP;
END;
/
```
```output
Department 20, salary at least 2000:
  FORD 3000
  SCOTT 3000
  JONES 2975
Department 10, any salary:
  KING 5000
  CLARK 2450
  MILLER 1300

PL/SQL procedure successfully completed.
```

Because the cursor is opened and closed automatically by each FOR loop, the same declaration serves both loops. With explicit control, a cursor must be **closed** before it is opened again with new parameters, or `CURSOR_ALREADY_OPEN` is raised.

## 4.5 Nested cursors

Processing a **master-detail** relation (each department with its employees) needs a cursor inside a cursor loop. The inner cursor takes the outer row's key as a parameter, so it is re-executed for every outer row.

```plsql
DECLARE
  CURSOR c_dept IS SELECT deptno, dname FROM dept ORDER BY deptno;
  CURSOR c_emp (p_dno NUMBER) IS
    SELECT ename, sal FROM emp WHERE deptno = p_dno ORDER BY ename;
  v_total NUMBER;
  v_count PLS_INTEGER;
BEGIN
  FOR d IN c_dept LOOP                               -- outer loop: one pass per department
    DBMS_OUTPUT.PUT_LINE('Department ' || d.deptno || ' ' || d.dname);
    v_total := 0;  v_count := 0;
    FOR e IN c_emp(d.deptno) LOOP                    -- inner loop: that department's employees
      DBMS_OUTPUT.PUT_LINE('   ' || RPAD(e.ename, 8) || e.sal);
      v_total := v_total + e.sal;
      v_count := v_count + 1;
    END LOOP;
    DBMS_OUTPUT.PUT_LINE('   -> ' || v_count || ' employees, total ' || v_total);
  END LOOP;
END;
/
```
```output
Department 10 ACCOUNTING
   CLARK   2450
   KING    5000
   MILLER  1300
   -> 3 employees, total 8750
Department 20 RESEARCH
   ADAMS   1100
   FORD    3000
   JONES   2975
   SCOTT   3000
   SMITH   800
   -> 5 employees, total 10875
Department 30 SALES
   ALLEN   1600
   BLAKE   2850
   JAMES   950
   MARTIN  1250
   TURNER  1500
   WARD    1250
   -> 6 employees, total 9400
Department 40 OPERATIONS
   -> 0 employees, total 0

PL/SQL procedure successfully completed.
```

Note department 40: the outer loop still visits it and the inner loop simply has no rows. The inner query runs four times here (once per department), so for large tables a **join** with `ORDER BY` and a control-break test is usually faster than a nested cursor; the nested form is chosen for clarity and when the inner work differs from row to row. A mistake to avoid: re-using the **same** cursor name for inner and outer loops.

## 4.6 FOR UPDATE and WHERE CURRENT OF

To change the row that the cursor is on, declare the cursor `FOR UPDATE`. Oracle then **locks** the selected rows when the cursor is opened, and `WHERE CURRENT OF cursor_name` applies an UPDATE or DELETE to exactly the last fetched row, without repeating the key condition.

```plsql
DECLARE
  CURSOR c_clerks IS
    SELECT empno, ename, sal FROM emp
    WHERE  job = 'CLERK' AND deptno = 20
    ORDER  BY ename
    FOR UPDATE OF sal NOWAIT;                     -- lock the rows; do not wait if another session holds them
BEGIN
  FOR r IN c_clerks LOOP
    UPDATE emp SET sal = sal * 1.10 WHERE CURRENT OF c_clerks;
    DBMS_OUTPUT.PUT_LINE(r.ename || ': ' || r.sal || ' -> ' || r.sal * 1.10);
  END LOOP;
  ROLLBACK;                                       -- release the locks, keep the demo data unchanged
END;
/
```
```output
ADAMS: 1100 -> 1210
SMITH: 800 -> 880

PL/SQL procedure successfully completed.
```

Points to remember. `NOWAIT` raises `ORA-00054: resource busy` at once instead of waiting; `WAIT n` waits n seconds. The locks last until `COMMIT` or `ROLLBACK`. **Committing inside the loop** releases the locks and the next FETCH raises `ORA-01002: fetch out of sequence`, so commit after the loop. `FOR UPDATE` must name no aggregate or DISTINCT in its query.

## 4.7 Cursor variables and bulk fetch (a short look)

A **REF cursor** (cursor variable) is a pointer to a query that can be chosen at run time and handed to another program or to a client application. The predefined type `SYS_REFCURSOR` can be used without declaring a type.

```plsql
DECLARE
  v_cur  SYS_REFCURSOR;
  v_name emp.ename%TYPE;
  v_choice VARCHAR2(5) := 'DEPT';
BEGIN
  IF v_choice = 'DEPT' THEN
    OPEN v_cur FOR SELECT dname FROM dept WHERE deptno = 10;
  ELSE
    OPEN v_cur FOR SELECT ename FROM emp WHERE deptno = 10;
  END IF;
  FETCH v_cur INTO v_name;
  DBMS_OUTPUT.PUT_LINE('First value: ' || v_name);
  CLOSE v_cur;
END;
/
```
```output
First value: ACCOUNTING
```

A function that returns `SYS_REFCURSOR` is how Java or PHP programs receive a result set from Oracle. For speed, **`BULK COLLECT`** fetches many rows in one step into a collection instead of one row per FETCH, which cuts the switching between the PL/SQL and SQL engines:

```plsql
DECLARE
  TYPE t_names IS TABLE OF emp.ename%TYPE;
  v_names t_names;
BEGIN
  SELECT ename BULK COLLECT INTO v_names FROM emp WHERE deptno = 10 ORDER BY ename;
  DBMS_OUTPUT.PUT_LINE(v_names.COUNT || ' names, the last is ' || v_names(v_names.LAST));
END;
/
```
```output
3 names, the last is MILLER
```

For very large result sets, fetch with `FETCH c BULK COLLECT INTO coll LIMIT 100;` in a loop so that memory use stays bounded.

## 4.8 Summary and exercises

A cursor is a handle on a context area. Implicit cursors serve DML and `SELECT INTO`; explicit cursors serve multi-row queries and are processed by DECLARE, OPEN, FETCH and CLOSE, with the attributes `%ISOPEN`, `%FOUND`, `%NOTFOUND` and `%ROWCOUNT`. The cursor FOR loop does the four steps for you. Parameters make one cursor reusable, nested cursors process master-detail data, and `FOR UPDATE` with `WHERE CURRENT OF` changes the fetched row under lock. REF cursors pass result sets around and `BULK COLLECT` fetches in bulk.

1. What is a cursor? Distinguish implicit and explicit cursors.
2. Explain the four steps of using an explicit cursor with a program that lists the employees of department 20.
3. Explain `%FOUND`, `%NOTFOUND`, `%ISOPEN` and `%ROWCOUNT`. Why is `%NOTFOUND` tested right after FETCH?
4. What errors occur if a cursor is opened twice, or fetched after CLOSE?
5. Write one block that prints the employees of department 30 using (a) a simple loop, (b) a WHILE loop and (c) a cursor FOR loop, and compare the three.
6. Why is the cursor FOR loop preferred? What does Oracle do for you?
7. Write a parameterised cursor that takes a job and a minimum salary, and use it twice with different values.
8. Write nested cursors that print each department with its employees and the department's average salary.
9. What is `FOR UPDATE`? Explain `WHERE CURRENT OF` and `NOWAIT` with an example. Why must COMMIT not be placed inside the loop?
10. What is a REF cursor? What is the advantage of `BULK COLLECT`?
11. A block fetches from a cursor over EMP with no `EXIT WHEN %NOTFOUND`. What happens?
12. Write a block using a cursor to print the top three salaries of EMP (name and salary) in descending order.

**Answers to the numerical items.** (5) the department 30 payroll printed by the WHILE version is 9,400 over 6 rows. (8) the averages are 2,916.67 (department 10), 2,175 (department 20), 1,566.67 (department 30) and none for department 40 (guard against a count of 0). (11) the loop never ends: after the last row each FETCH leaves the variables unchanged and `%NOTFOUND` is never tested, so the last row is processed again and again. (12) KING 5000, then FORD and SCOTT 3000 (either order unless a second sort key is given).

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the attributes of an explicit cursor.**

`c%ISOPEN` is TRUE when the cursor is open. `c%FOUND` is TRUE when the last FETCH returned a row and is NULL before the first fetch. `c%NOTFOUND` is TRUE when the last FETCH returned no row, and is used to leave the loop. `c%ROWCOUNT` counts the rows fetched so far. Example: in `LOOP FETCH c INTO v; EXIT WHEN c%NOTFOUND; ... END LOOP;` the loop ends after the last row, and `c%ROWCOUNT` then gives the number of rows. The same attributes exist for the implicit cursor as `SQL%FOUND` and so on.

**Q2 (5 marks). What is a parameterised cursor? Give an example.**

A parameterised cursor takes values when it is opened, so one declaration serves many queries. `CURSOR c_pay (p_dno NUMBER, p_min NUMBER DEFAULT 0) IS SELECT ename, sal FROM emp WHERE deptno = p_dno AND sal >= p_min;` is opened as `OPEN c_pay(20, 2000)` or used as `FOR r IN c_pay(10) LOOP ...`. Parameters are read-only, may have defaults and can appear only where a literal could appear in the query. For department 20 with a minimum of 2000 the cursor returns FORD, SCOTT and JONES.

**Q3 (10 marks). Describe the types of cursors and the steps of using an explicit cursor, with an example.**

*Introduction.* Oracle processes each SQL statement in a context area, and a cursor is the handle to it.

*Types.* Implicit cursors are created by Oracle for DML and `SELECT INTO` and expose `SQL%ROWCOUNT`, `SQL%FOUND` and `SQL%NOTFOUND`. Explicit cursors are declared by the programmer for multi-row queries. Cursor variables (REF cursors) can point to different queries at run time.

*Steps.* Declare the cursor with its SELECT, open it (the query runs), fetch rows into variables or a record one at a time, and close it to free the area. The attributes `%FOUND`, `%NOTFOUND`, `%ISOPEN` and `%ROWCOUNT` describe its state.

*Example.* A block declares `c_emp` over the employees of department 10, opens it, loops with FETCH and `EXIT WHEN c_emp%NOTFOUND`, prints CLARK, KING and MILLER and closes the cursor.

*Cursor FOR loop.* It opens, fetches and closes automatically and declares its own record.

*Conclusion.* Cursors let a procedural program process a set of rows one at a time.

**Q4 (10 marks). Explain nested cursors and the FOR UPDATE clause with examples.**

*Nested cursors.* An inner cursor, normally parameterised, is opened for each row of an outer cursor, to process master-detail data. Example: the outer cursor lists the four departments, the inner cursor `c_emp(p_dno)` lists the employees of each and a running total is printed: 8750 for department 10, 10875 for 20, 9400 for 30 and 0 employees for 40.

*FOR UPDATE.* Declaring `SELECT ... FOR UPDATE OF sal NOWAIT` locks the selected rows at OPEN; `NOWAIT` fails at once with ORA-00054 if another session holds a lock. Inside the loop, `UPDATE emp SET sal = sal * 1.10 WHERE CURRENT OF c_clerks;` changes exactly the row last fetched, so no key condition is needed.

*Care.* The locks last until COMMIT or ROLLBACK, so a COMMIT inside the loop makes the next FETCH fail with ORA-01002.

*Conclusion.* Nested cursors give structured reports, and FOR UPDATE with WHERE CURRENT OF gives safe row-by-row updates.
