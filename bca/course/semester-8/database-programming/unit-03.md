---
subject: Database Programming
grade: BCA Semester 8 (Elective III)
unit: 3
title: PL/SQL Exception
hours: 5
area: BCA 453 · Database Programming · Unit 3
---

A payroll program that stops with a raw `ORA-01403: no data found` message on the screen is a program nobody trusts. Errors will happen: an employee number that does not exist, a division by zero, a duplicate key, a business rule that is broken. The question is only whether the program handles them or falls over. PL/SQL treats every run-time error as an **exception**, an event that interrupts the normal flow and jumps to a handler you wrote.

::: key What this unit gives you
- What an exception is, and the predefined, non-predefined and user-defined kinds.
- The `EXCEPTION` section, `WHEN ... THEN` handlers, `WHEN OTHERS`, `SQLCODE` and `SQLERRM`.
- Scope and propagation of exceptions through nested blocks.
- `RAISE`, `RAISE_APPLICATION_ERROR` and `PRAGMA EXCEPTION_INIT` for your own errors.
:::

## 3.1 What an exception is

Two kinds of errors occur in a PL/SQL program. A **compile-time error** (a missing semicolon, an unknown column) is found by the compiler before anything runs. A **run-time error** appears while the program executes, for instance a `SELECT INTO` that finds no row. Run-time errors are called **exceptions**. When one is **raised**, normal execution stops, control goes to the `EXCEPTION` section of the current block, and the matching handler runs. After a handler finishes, the block ends: control does **not** return to the statement that failed.

```plsql
BEGIN
  statements ...
EXCEPTION
  WHEN exception_name1 THEN handler statements ...
  WHEN exception_name2 OR exception_name3 THEN handler statements ...
  WHEN OTHERS THEN handler statements ...        -- anything not listed above, always last
END;
```

**Kinds of exceptions**

| Kind | Raised by | Has a name? | Example |
|---|---|---|---|
| **Predefined** (named system) | Oracle, automatically | Yes, in package STANDARD | `NO_DATA_FOUND`, `ZERO_DIVIDE` |
| **Non-predefined** | Oracle, automatically | No, only an ORA number until you name it | `ORA-02292` child record found |
| **User-defined** | Your code, with `RAISE` | Yes, you declare it | `e_salary_too_high` |

**The common predefined exceptions**

| Exception | Error | When it is raised |
|---|---|---|
| `NO_DATA_FOUND` | ORA-01403 | `SELECT INTO` returns no row, or a deleted collection element is read |
| `TOO_MANY_ROWS` | ORA-01422 | `SELECT INTO` returns more than one row |
| `ZERO_DIVIDE` | ORA-01476 | Division by zero |
| `DUP_VAL_ON_INDEX` | ORA-00001 | Insert or update would duplicate a unique or primary key |
| `INVALID_NUMBER` | ORA-01722 | Conversion of a text to a number fails, in a SQL statement |
| `VALUE_ERROR` | ORA-06502 | Conversion, truncation or size error in a PL/SQL assignment |
| `CURSOR_ALREADY_OPEN` | ORA-06511 | Opening a cursor that is open |
| `INVALID_CURSOR` | ORA-01001 | Fetching from or closing a cursor that is not open |
| `LOGIN_DENIED` | ORA-01017 | Wrong user name or password |
| `CASE_NOT_FOUND` | ORA-06592 | A CASE statement has no matching WHEN and no ELSE |
| `ACCESS_INTO_NULL` | ORA-06530 | Assigning to a field of an uninitialised object |
| `PROGRAM_ERROR` | ORA-06501 | An internal PL/SQL problem |
| `STORAGE_ERROR` | ORA-06500 | Out of memory |
| `TIMEOUT_ON_RESOURCE` | ORA-00051 | A wait for a resource timed out |

Two are easy to confuse. `INVALID_NUMBER` is raised in **SQL** statements (`WHERE sal = 'abc'`), while `VALUE_ERROR` is raised in **procedural** statements (`v_n := 'abc';`).

## 3.2 Handling exceptions

```plsql
SQL> DECLARE
  2    v_ename emp.ename%TYPE;
  3  BEGIN
  4    SELECT ename INTO v_ename FROM emp WHERE empno = &empno;
  5    DBMS_OUTPUT.PUT_LINE('Employee: ' || v_ename);
  6  EXCEPTION
  7    WHEN NO_DATA_FOUND THEN
  8      DBMS_OUTPUT.PUT_LINE('There is no employee with that number');
  9    WHEN TOO_MANY_ROWS THEN
 10      DBMS_OUTPUT.PUT_LINE('More than one employee matched');
 11  END;
 12  /
```

| Entered | Result |
|---|---|
| `7369` | `Employee: SMITH` |
| `9999` | `There is no employee with that number` |

If line 4 used `WHERE deptno = &dno` and the user entered 10, three rows would be found and the output would be `More than one employee matched`.

**WHEN OTHERS, SQLCODE and SQLERRM.** `OTHERS` catches every exception not named earlier, and must be the **last** handler. Two functions describe the exception being handled:

| Function | Returns |
|---|---|
| `SQLCODE` | The error number: negative for ORA errors (for example -1476), `+100` for `NO_DATA_FOUND`, `+1` for a user-defined exception, 0 for no error |
| `SQLERRM` | The message text, for example `ORA-01476: divisor is equal to zero` |

They cannot be used directly inside an SQL statement; copy them to variables first.

```plsql
DECLARE
  v_comm NUMBER;
  v_ratio NUMBER;
  v_code  NUMBER;
  v_msg   VARCHAR2(200);
BEGIN
  SELECT comm INTO v_comm FROM emp WHERE ename = 'TURNER';   -- his commission is 0
  v_ratio := 1500 / v_comm;                                  -- division by zero
  DBMS_OUTPUT.PUT_LINE('ratio = ' || v_ratio);
EXCEPTION
  WHEN ZERO_DIVIDE THEN
    DBMS_OUTPUT.PUT_LINE('Cannot divide by a zero commission');
  WHEN OTHERS THEN
    v_code := SQLCODE;  v_msg := SQLERRM;
    DBMS_OUTPUT.PUT_LINE('Unexpected error ' || v_code || ': ' || v_msg);
END;
/
```
```output
Cannot divide by a zero commission

PL/SQL procedure successfully completed.
```

The exception is **handled**, so Oracle reports success. If the handler is changed to `WHEN OTHERS` only, the output becomes `Unexpected error -1476: ORA-01476: divisor is equal to zero`. Handlers are chosen in order, so a specific name placed after `OTHERS` is a compile error (PLS-00370).

A frequent task is reacting to a duplicate key:

```plsql
BEGIN
  INSERT INTO emp (empno, ename, deptno) VALUES (7369, 'NEW PERSON', 20);   -- 7369 is SMITH
  DBMS_OUTPUT.PUT_LINE('Inserted');
EXCEPTION
  WHEN DUP_VAL_ON_INDEX THEN
    DBMS_OUTPUT.PUT_LINE('Employee number 7369 already exists, nothing inserted');
END;
/
```
```output
Employee number 7369 already exists, nothing inserted

PL/SQL procedure successfully completed.
```

::: tip Exam tip
Questions about exceptions usually want: the three kinds, the syntax of the EXCEPTION section, at least four predefined names with their causes, and one worked example. Say that after the handler runs the block **ends**.
:::

## 3.3 Exception scope

An exception name is **declared** (predefined ones are declared for you) and obeys the same scope rules as a variable.

1. A name declared in a block is visible in that block and in blocks nested in it, but not outside.
2. A handler of a block catches exceptions raised in that block's **executable** section only.
3. An exception raised in the **declaration** section (for example `v_small NUMBER(2) := 500;`) or inside an **exception handler** is **not** caught by handlers of the same block; it propagates to the enclosing block.
4. A user-defined exception declared in an inner block cannot be named in the outer block's handler; only `WHEN OTHERS` there can catch it.
5. A local name that is the same as a predefined one hides it, which is a common source of confusion: never declare your own `NO_DATA_FOUND`.

```plsql
DECLARE
  v_small NUMBER(2) := 500;          -- raises VALUE_ERROR while the block is being set up
BEGIN
  DBMS_OUTPUT.PUT_LINE('never reached');
EXCEPTION
  WHEN VALUE_ERROR THEN
    DBMS_OUTPUT.PUT_LINE('never reached either');   -- this block's own handler does NOT run
END;
/
```

Run on its own, this block ends with `ORA-06502: PL/SQL: numeric or value error: number precision too large` and `ORA-06512: at line 2`, because the error happened in the declaration. Placed inside another block that has a `VALUE_ERROR` handler, the **outer** handler would catch it.

## 3.4 User-defined exceptions

Business rules are not Oracle errors, but you can make them behave like errors. Three steps: **declare** the exception, **raise** it with `RAISE` when the rule is broken, and **handle** it by name.

```plsql
DECLARE
  e_cap        EXCEPTION;                        -- 1. declare
  c_max_sal    CONSTANT NUMBER := 5000;
  v_sal        emp.sal%TYPE;
  v_new_sal    emp.sal%TYPE;
BEGIN
  SELECT sal INTO v_sal FROM emp WHERE empno = &empno;
  v_new_sal := v_sal * (1 + &percent / 100);
  IF v_new_sal > c_max_sal THEN
    RAISE e_cap;                                 -- 2. raise
  END IF;
  UPDATE emp SET sal = v_new_sal WHERE empno = &empno;
  DBMS_OUTPUT.PUT_LINE('New salary ' || v_new_sal);
  ROLLBACK;
EXCEPTION
  WHEN e_cap THEN                                -- 3. handle
    DBMS_OUTPUT.PUT_LINE('Raise rejected: new salary ' || v_new_sal || ' exceeds the cap of ' || c_max_sal);
  WHEN NO_DATA_FOUND THEN
    DBMS_OUTPUT.PUT_LINE('No such employee');
END;
/
```

| empno | percent | Calculation | Output |
|---|---|---|---|
| 7788 (SCOTT, 3000) | 10 | 3000 x 1.10 = 3300 | `New salary 3300` |
| 7788 (SCOTT, 3000) | 80 | 3000 x 1.80 = 5400 | `Raise rejected: new salary 5400 exceeds the cap of 5000` |
| 9999 | 10 | no row | `No such employee` |

A user-defined exception has `SQLCODE` +1 and `SQLERRM` equal to `User-Defined Exception`. A bare `RAISE;` inside a handler **re-raises** the exception being handled, which is how you log an error and still let the caller know.

## 3.5 Exception propagation

When an exception is raised and the current block has **no matching handler**, it **propagates**: the block ends and the same exception is raised again in the **enclosing** block (or, for a called subprogram, in the caller). The search continues outward until a handler is found. If none exists, the exception reaches the host (SQL*Plus), which prints the error, and the unhandled statement's work is rolled back.

```plsql
DECLARE
  v_zero NUMBER := 0;
  v_x    NUMBER;
BEGIN
  DBMS_OUTPUT.PUT_LINE('Outer block starts');
  BEGIN
    DBMS_OUTPUT.PUT_LINE('Inner block starts');
    v_x := 10 / v_zero;                          -- raises ZERO_DIVIDE
    DBMS_OUTPUT.PUT_LINE('never printed');
  EXCEPTION
    WHEN NO_DATA_FOUND THEN                      -- the wrong handler: no match
      DBMS_OUTPUT.PUT_LINE('inner handler');
  END;
  DBMS_OUTPUT.PUT_LINE('never printed either');  -- the inner block ended with an error
EXCEPTION
  WHEN ZERO_DIVIDE THEN
    DBMS_OUTPUT.PUT_LINE('Outer handler caught: ' || SQLERRM);
END;
/
```
```output
Outer block starts
Inner block starts
Outer handler caught: ORA-01476: divisor is equal to zero

PL/SQL procedure successfully completed.
```

To **continue** after an error, enclose the risky statement in its own small block with its own handler. The loop below tries to divide 100 by each of 5, 0 and 20, and carries on after the zero:

```plsql
DECLARE
  TYPE t_nums IS TABLE OF NUMBER;
  v_div t_nums := t_nums(5, 0, 20);
BEGIN
  FOR i IN 1..v_div.COUNT LOOP
    BEGIN
      DBMS_OUTPUT.PUT_LINE('100 / ' || v_div(i) || ' = ' || 100 / v_div(i));
    EXCEPTION
      WHEN ZERO_DIVIDE THEN
        DBMS_OUTPUT.PUT_LINE('100 / ' || v_div(i) || ' : skipped, divisor is zero');
    END;
  END LOOP;
END;
/
```
```output
100 / 5 = 20
100 / 0 : skipped, divisor is zero
100 / 20 = 5

PL/SQL procedure successfully completed.
```

**An error inside a handler** propagates outward as well, so a handler should be short and safe. To log and pass an error on, write the log statement and then `RAISE;`:

```plsql
EXCEPTION
  WHEN OTHERS THEN
    INSERT INTO error_log (when_happened, code, message) VALUES (SYSDATE, SQLCODE, SQLERRM);
    RAISE;          -- the caller still sees the original error
```

(The logging row is part of the transaction that is then rolled back; to keep it, the logger is written as an **autonomous transaction**, a procedure with `PRAGMA AUTONOMOUS_TRANSACTION` that commits on its own.) `DBMS_UTILITY.FORMAT_ERROR_BACKTRACE` returns the line numbers where the error started, which `SQLERRM` does not.

## 3.6 Advanced exception concepts

**RAISE_APPLICATION_ERROR.** To send **your own** error number and message to the caller, as if Oracle had raised it, call

```plsql
RAISE_APPLICATION_ERROR(error_number, message [, keep_errors]);
```

`error_number` must lie between **-20000 and -20999**; the message is at most 2,048 bytes. The call ends the block and propagates the error; the caller can test `SQLCODE` or catch it with `WHEN OTHERS`. It is how stored procedures and triggers report business errors to applications.

```plsql
SQL> DECLARE
  2    v_sal NUMBER := -50;
  3  BEGIN
  4    IF v_sal <= 0 THEN
  5      RAISE_APPLICATION_ERROR(-20001, 'Salary must be positive');
  6    END IF;
  7  END;
  8  /
DECLARE
*
ERROR at line 1:
ORA-20001: Salary must be positive
ORA-06512: at line 5
```

`ORA-06512` is the call-stack line that Oracle adds: the error came from line 5.

**PRAGMA EXCEPTION_INIT.** Many Oracle errors have a number but no name, for instance `ORA-02292: integrity constraint violated - child record found`, raised when you delete a department that still has employees. A **pragma** is an instruction to the compiler. `EXCEPTION_INIT` links a name you declare to an error number, so that you can write a normal handler:

```plsql
DECLARE
  e_has_children EXCEPTION;
  PRAGMA EXCEPTION_INIT(e_has_children, -2292);   -- the pragma goes in the declaration section
BEGIN
  DELETE FROM dept WHERE deptno = 10;             -- EMP rows still refer to department 10
  DBMS_OUTPUT.PUT_LINE('Department deleted');
EXCEPTION
  WHEN e_has_children THEN
    DBMS_OUTPUT.PUT_LINE('Cannot delete department 10: it still has employees');
END;
/
```
```output
Cannot delete department 10: it still has employees

PL/SQL procedure successfully completed.
```

The same technique names `ORA-01400` (cannot insert NULL), `ORA-02291` (parent key not found) and `ORA-00054` (resource busy, NOWAIT). The pragma can also be used with an error number raised by `RAISE_APPLICATION_ERROR`, so that callers can catch `-20001` by name.

| Tool | Purpose | Number range |
|---|---|---|
| Predefined exceptions | Common Oracle errors, already named | fixed ORA numbers |
| `EXCEPTION_INIT` | Name an Oracle error that has no name | any ORA number you choose to name |
| `RAISE` with a declared exception | Signal a rule break inside the same program | `SQLCODE` = +1 |
| `RAISE_APPLICATION_ERROR` | Signal a rule break to the **caller** with number and message | -20000 to -20999 |

**Good practice.** Handle specific exceptions before `OTHERS`; never write `WHEN OTHERS THEN NULL;` because it hides every bug; log and re-raise what you cannot repair; put each risky statement that should not stop a loop in its own block; and keep the transaction decision (COMMIT or ROLLBACK) in one place.

## 3.7 Summary and exercises

An exception is a run-time error. The `EXCEPTION` section holds `WHEN` handlers; the first match runs and the block then ends. Predefined exceptions (`NO_DATA_FOUND`, `TOO_MANY_ROWS`, `ZERO_DIVIDE`, `DUP_VAL_ON_INDEX`, `INVALID_NUMBER`, `VALUE_ERROR` ...) are named by Oracle; others are named with `EXCEPTION_INIT`; user-defined ones are declared and raised with `RAISE`. `SQLCODE` and `SQLERRM` describe the current error. An unhandled exception propagates outward; errors in the declaration section or in a handler escape the same block. `RAISE_APPLICATION_ERROR` sends a -20000 to -20999 error to the caller.

1. Define exception. Distinguish compile-time and run-time errors.
2. Name the three kinds of exceptions and give an example of each.
3. Write the general syntax of the EXCEPTION section. In what order must the handlers appear, and why is OTHERS last?
4. List six predefined exceptions with their ORA numbers and causes.
5. What is the difference between `INVALID_NUMBER` and `VALUE_ERROR`?
6. What do `SQLCODE` and `SQLERRM` return? Why can they not be used directly in an INSERT statement?
7. Write a block that reads an employee by number and prints a message for `NO_DATA_FOUND`.
8. Explain exception scope. What happens to an exception raised in the declaration section?
9. Write a block that defines `e_negative`, raises it when a given amount is below zero, and handles it.
10. What is exception propagation? Write nested blocks that show an exception caught by the outer block.
11. How can a loop continue with the next item after one item raises an error?
12. Explain `RAISE_APPLICATION_ERROR` with its number range and an example. How does it differ from `RAISE`?
13. Explain `PRAGMA EXCEPTION_INIT` by handling `ORA-02292` when deleting a department.
14. Why is `WHEN OTHERS THEN NULL;` poor practice?

**Answers to the numerical items.** (3) specific handlers first, `OTHERS` last, because the first matching handler runs and `OTHERS` matches everything; a handler after it is unreachable (PLS-00370). (4) see the table in Section 3.1: for example ORA-01403, ORA-01422, ORA-01476, ORA-00001, ORA-01722, ORA-06502. (5) `INVALID_NUMBER` arises in SQL statements, `VALUE_ERROR` in procedural statements. (6) `SQLCODE` is the error number (+100 for NO_DATA_FOUND, +1 for user-defined), `SQLERRM` the message; copy them to variables because SQL statements cannot call them.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain predefined and user-defined exceptions.**

Predefined exceptions are named by Oracle and raised automatically, for example `NO_DATA_FOUND` (SELECT INTO finds no row), `TOO_MANY_ROWS`, `ZERO_DIVIDE` and `DUP_VAL_ON_INDEX`. A user-defined exception is declared in the DECLARE section as `e_name EXCEPTION;`, raised explicitly by `RAISE e_name;` when a business rule is broken, and handled in the EXCEPTION section by `WHEN e_name THEN`. Example: `RAISE e_cap` when a new salary exceeds 5000, handled by printing a rejection message. Its SQLCODE is +1.

**Q2 (5 marks). Explain RAISE_APPLICATION_ERROR.**

`RAISE_APPLICATION_ERROR(error_number, message)` stops the block and returns an error with a number from -20000 to -20999 and the given text to the caller, as if it were an Oracle error. Example: `RAISE_APPLICATION_ERROR(-20001, 'Salary must be positive');` makes SQL*Plus show `ORA-20001: Salary must be positive`. It is used in stored procedures and triggers to report business errors to applications; unlike a plain `RAISE` of a user-defined exception, it carries its own number and message and can be seen outside the program.

**Q3 (10 marks). Explain exception handling in PL/SQL with the types of exceptions and examples.**

*Introduction.* An exception is a run-time error that interrupts the block and transfers control to a handler in the EXCEPTION section; after the handler the block ends.

*Types.* Predefined (for example `NO_DATA_FOUND`), non-predefined (an ORA number named with `PRAGMA EXCEPTION_INIT`) and user-defined (declared and raised with `RAISE`).

*Syntax.* `EXCEPTION WHEN name THEN ... WHEN OTHERS THEN ...`, with OTHERS last, plus `SQLCODE` and `SQLERRM` for details.

*Example.* A SELECT INTO on `empno = 9999` raises `NO_DATA_FOUND` and the handler prints 'There is no employee with that number'. A salary raise that would exceed 5000 raises `e_cap`, which is handled by a rejection message.

*Propagation and scope.* An unhandled exception moves to the enclosing block; errors in the declaration section or in a handler escape the same block.

*Conclusion.* Handlers make programs robust and give users meaningful messages instead of raw ORA errors.

**Q4 (10 marks). Explain RAISE_APPLICATION_ERROR and PRAGMA EXCEPTION_INIT with examples.**

*Introduction.* Both extend the built-in set of exceptions: one issues your own error, the other gives a name to an existing Oracle error.

*RAISE_APPLICATION_ERROR.* Call with a number in -20000 to -20999 and a message; the error propagates to the caller and can be caught with `WHEN OTHERS` and tested by `SQLCODE`. Example: refusing a non-positive salary with -20001.

*PRAGMA EXCEPTION_INIT.* In the declaration section, `e_has_children EXCEPTION; PRAGMA EXCEPTION_INIT(e_has_children, -2292);` links the name to ORA-02292. A `DELETE FROM dept WHERE deptno = 10` then raises it, and `WHEN e_has_children THEN` prints 'Cannot delete department 10: it still has employees'.

*Comparison.* The first creates errors, the second catches existing ones; the first is used in triggers and procedures, the second in programs that run SQL that may fail on constraints.

*Conclusion.* Together with `RAISE` and the predefined exceptions they let a program signal and handle every error condition in a controlled way.
