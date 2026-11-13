---
subject: Database Programming
grade: BCA Semester 8 (Elective III)
unit: 2
title: PL/SQL
hours: 13
area: BCA 453 · Database Programming · Unit 2
---

SQL can say **what** you want: "the employees of department 10". It cannot say "if the employee is a clerk, give 5 percent, otherwise 8, and stop the loop when the budget is spent". For that you need variables, decisions and loops, and you want them to run **next to the data**. Oracle's answer is **PL/SQL** (Procedural Language extensions to SQL), a block-structured language in which SQL statements sit naturally inside ordinary programming constructs.

::: key What this unit gives you
- What PL/SQL is, how the PL/SQL engine and the SQL engine cooperate, and the structure of a block.
- Running a script, printing with `DBMS_OUTPUT.PUT_LINE`, and bringing values in with substitution variables.
- The language fundamentals: identifiers, literals, data types (`%TYPE`, `%ROWTYPE`), operators, NULL logic and scope.
- DML and transaction control inside PL/SQL, conditional control (IF, CASE) and repetitive control (simple, WHILE, FOR, nested loops, CONTINUE, labels).
:::

## 2.1 PL/SQL concepts and architecture

**PL/SQL** is Oracle's procedural extension of SQL. A PL/SQL program is written in **blocks**, each of which can declare variables, run SQL and procedural statements, and handle errors. It was first released with Oracle 6 and is the language of stored procedures, functions, packages and triggers.

**Why not just SQL, or just a client language?**

| Need | Plain SQL | Client program (Java, PHP) | PL/SQL |
|---|---|---|---|
| Variables, IF, loops | No | Yes | Yes |
| Many statements as one round trip | No | One trip per statement | One trip for the whole block |
| Data types identical to the database | n/a | Needs conversion | Same types, `%TYPE` follows column changes |
| Runs in the server, reused by all apps | n/a | Each app has its own copy | Stored once, shared, compiled once |
| Built-in error handling for SQL errors | No | Library dependent | `EXCEPTION` section |
| Security by controlled access | Table privileges only | Table privileges | `EXECUTE` on a program, no table access needed |

**Advantages of PL/SQL:** better performance because a block is sent as a unit; tight integration with SQL (a `SELECT ... INTO` needs no cursor code); portability across every platform that runs Oracle; modularity (procedures, functions, packages); and strong error handling.

**Architecture.** When a block reaches the server, the **PL/SQL engine** executes it. The engine itself runs the *procedural* statements (assignments, IF, loops, calls). Whenever it meets a *SQL* statement, it hands it to the **SQL statement executor**, which works on the data, and gets the result back. If the block came from a client such as SQL*Plus, the whole block crosses the network once.

```svgfig label="2.1" caption="Architecture of PL/SQL. The client sends one block; the PL/SQL engine runs the procedural statements and passes each SQL statement to the SQL executor."
f = Fig(640, 210)
f.box(10, 70, 120, 60, "Client\nSQL*Plus or\napplication", fill=SOFT, stroke=SLATE, size=10)
f.arrow([(130, 100), (190, 100)], color=NAVY, label="PL/SQL block", lpos=(160, 88))
f.box(190, 10, 330, 190, "", fill=SAND, stroke=AMBER)
f.text(355, 26, "ORACLE SERVER", size=10, anchor="middle", color=AMBER)
f.box(205, 46, 140, 130, "PL/SQL engine\n\nProcedural\nstatement\nexecutor", fill=BLUE, stroke=NAVY, size=10)
f.box(375, 46, 130, 60, "SQL statement\nexecutor", fill=MINT, stroke=TEAL, size=10)
f.box(375, 126, 130, 50, "Data files,\nbuffer cache", fill="#ffffff", stroke=TEAL, size=10)
f.arrow([(345, 76), (375, 76)], color=NAVY, label="SQL", lpos=(360, 66))
f.arrow([(440, 106), (440, 126)], color=TEAL, both=True)
f.arrow([(190, 170), (130, 170), (130, 130)], color=SLATE, dash=True, label="results", lpos=(162, 184))
```

## 2.2 Block structure

Every PL/SQL program is made of blocks. A block has up to four parts:

```plsql
DECLARE                      -- optional: variables, constants, cursors, local subprograms
   ...
BEGIN                        -- mandatory: the executable statements
   ...
EXCEPTION                    -- optional: what to do when an error is raised
   ...
END;                         -- mandatory, followed by ; (and / in SQL*Plus)
```

| Part | Keyword | Required? | Contains |
|---|---|---|---|
| Declarative | `DECLARE` | No | Names of variables, constants, cursors, user exceptions |
| Executable | `BEGIN ... END` | **Yes** | SQL and procedural statements, at least one statement |
| Exception handling | `EXCEPTION` | No | Handlers (Unit 3) |

There are two kinds of blocks.

- An **anonymous block** has no name, is compiled each time it is run and is not stored. It begins with `DECLARE` or `BEGIN`. You write these in the lab.
- A **named block** (procedure, function, package, trigger) is compiled once and **stored in the database**. It begins with a header such as `CREATE OR REPLACE PROCEDURE name IS` (Units 5 to 7).

Blocks can be **nested** inside the executable or exception section of another block. The inner block is a unit of its own: it may have its own declarations and handlers.

::: note Statement rules
Each statement ends with a semicolon. Keywords are not case sensitive (`begin` = `BEGIN`), but text literals are: `'SMITH'` is not `'smith'`. A block that has nothing to do must still contain `NULL;` as a statement, because the executable section cannot be empty.
:::

## 2.3 Executing a script and DBMS_OUTPUT.PUT_LINE

A block typed in SQL*Plus is finished by `/` on a line by itself. Output is produced by the supplied package **DBMS_OUTPUT**:

| Subprogram | Effect |
|---|---|
| `DBMS_OUTPUT.PUT_LINE(text)` | Puts the text and a line end into a buffer |
| `DBMS_OUTPUT.PUT(text)` | Puts text without a line end |
| `DBMS_OUTPUT.NEW_LINE` | Ends the current line |
| `DBMS_OUTPUT.ENABLE(n)` / `DISABLE` | Sets the buffer size (up to 1,000,000 bytes) or turns buffering off |

SQL*Plus prints the buffer **after** the block finishes, and only if `SET SERVEROUTPUT ON` has been issued. A line can hold at most 32,767 bytes. The argument is one string: join pieces with the concatenation operator `||`; numbers are converted automatically.

```plsql
SQL> SET SERVEROUTPUT ON
SQL> BEGIN
  2    DBMS_OUTPUT.PUT_LINE('Hello, Database Programming');
  3    DBMS_OUTPUT.PUT_LINE('2 + 3 = ' || (2 + 3));
  4  END;
  5  /
Hello, Database Programming
2 + 3 = 5

PL/SQL procedure successfully completed.
```

The last line is Oracle's reply to every block that finishes without an unhandled error. Save a block as `hello.sql` (the file ends with `/`) and run it with `@hello`.

**Compile errors.** If the block contains a syntax mistake, nothing runs and Oracle reports the line and the PLS or ORA code:

```plsql
SQL> DECLARE
  2    v_x NUMBER := 10
  3  BEGIN
  4    NULL;
  5  END;
  6  /
  v_x NUMBER := 10
*
ERROR at line 2:
ORA-06550: line 3, column 1:
PLS-00103: Encountered the symbol "BEGIN" when expecting one of the following:
...
```

The cause is the missing semicolon at the end of line 2; the error is reported at the next token. (The listing of expected symbols is long and is shortened here.) For a **stored** program, the message is "Warning: Procedure created with compilation errors" and `SHOW ERRORS` lists them.

## 2.4 The substitution variable feature

Unit 1 showed `&` in SQL statements. In PL/SQL it works the same way: SQL*Plus replaces `&name` by the entered text **before** the block is sent to the server, so the server sees an ordinary literal.

```plsql
SQL> SET VERIFY ON
SQL> DECLARE
  2    v_ename  emp.ename%TYPE;
  3    v_annual NUMBER(9,2);
  4  BEGIN
  5    SELECT ename, sal * 12 INTO v_ename, v_annual
  6    FROM   emp
  7    WHERE  empno = &empno;
  8    DBMS_OUTPUT.PUT_LINE(v_ename || ' earns ' || v_annual || ' a year');
  9  END;
 10  /
Enter value for empno: 7369
old   7:   WHERE  empno = &empno;
new   7:   WHERE  empno = 7369;
SMITH earns 9600 a year

PL/SQL procedure successfully completed.
```

Because the text is pasted in, a character value needs quotes in the **block**: `v_job := '&job';`. A number is pasted as is: `v_n := &n;`. Entering `abc` for a number gives a compile error, not a run-time error. Two other ways to pass values in:

- **Bind variables** declared in SQL*Plus: `VARIABLE b_dno NUMBER`, then `EXEC :b_dno := 20` and use `:b_dno` inside the block. A bind variable is a real parameter, so Oracle reuses the parsed statement and it is safe from injection; `PRINT b_dno` displays it.
- **Procedure parameters** (Unit 6), the normal way in applications.

## 2.5 PL/SQL language fundamentals

**Character set and lexical units.** The units of a program are identifiers, reserved words, literals, delimiters and comments.

| Unit | Rules and examples |
|---|---|
| **Identifier** | Starts with a letter, then letters, digits, `$`, `_`, `#`; at most 30 bytes (128 from Oracle 12.2); case-insensitive; must not be a reserved word (`BEGIN`, `LOOP`, `SELECT`). Quoted identifiers (`"Total Pay"`) allow spaces and case, and are best avoided. |
| **Numeric literal** | `25`, `-3.14`, `6.02E23` |
| **Character literal** | `'Kathmandu'`; a quote inside is doubled: `'It''s'`; alternative quoting: `q'[It's]'` |
| **Boolean literal** | `TRUE`, `FALSE`, `NULL` |
| **Comment** | `-- to end of line`, or `/* over several lines */` |
| **Delimiters** | `+ - * / ** = < > <= >= <> != := => .. || ; , ( ) %` |

**Data types.** Scalar types hold one value. The common ones:

| Type | Notes |
|---|---|
| `NUMBER(p,s)` | Same as the SQL type |
| `PLS_INTEGER` (`BINARY_INTEGER`) | Whole numbers, fast for counters and loops, range $-2^{31}$ to $2^{31}-1$ |
| `VARCHAR2(n)` | Up to 32,767 bytes in PL/SQL (4000 as a column) |
| `CHAR(n)`, `DATE`, `TIMESTAMP` | As in SQL |
| `BOOLEAN` | `TRUE`, `FALSE`, `NULL`; **PL/SQL only** (not a column type in versions before 23ai) |

**Anchored declarations** make variables follow the database:

```plsql
v_sal     emp.sal%TYPE;     -- same type as the column EMP.SAL
v_emp     emp%ROWTYPE;      -- a record with one field per column of EMP
v_total   v_sal%TYPE;       -- same type as another variable
```

If the column is later changed from `NUMBER(7,2)` to `NUMBER(9,2)` the program needs no edit; this is the reason to prefer `%TYPE`.

**Variables and constants**

```plsql
DECLARE
  c_rate     CONSTANT NUMBER(4,3) := 0.13;      -- a constant must be given a value
  v_name     VARCHAR2(20) := 'Sita';            -- initial value with :=
  v_count    PLS_INTEGER DEFAULT 0;             -- DEFAULT is the same as :=
  v_flag     BOOLEAN;                           -- not initialised: NULL
  v_id       NUMBER NOT NULL := 1;              -- NOT NULL needs an initial value
```

An uninitialised variable is **NULL**. Assignment uses `:=`. A name of a variable should not equal a column name used in an embedded SQL statement: in `WHERE ename = ename` both sides are the column, so every row matches. Use prefixes (`v_`, `c_`, `p_`) as the examples do.

**Operators and precedence** (highest first):

| Order | Operators |
|---|---|
| 1 | `**` (exponent) |
| 2 | unary `+`, `-` |
| 3 | `*`, `/` |
| 4 | `+`, `-`, `||` |
| 5 | `=`, `<`, `>`, `<=`, `>=`, `<>`, `!=`, `IS NULL`, `LIKE`, `BETWEEN`, `IN` |
| 6 | `NOT` |
| 7 | `AND` |
| 8 | `OR` |

**NULL logic.** NULL means "unknown", so any comparison with NULL is neither true nor false; it is NULL. An `IF` runs its THEN part only when the condition is **TRUE**, so NULL behaves like FALSE.

| a | b | a AND b | a OR b | NOT a |
|---|---|---|---|---|
| TRUE | NULL | NULL | TRUE | FALSE |
| FALSE | NULL | FALSE | NULL | TRUE |
| NULL | NULL | NULL | NULL | NULL |

Test with `IS NULL` and `IS NOT NULL`, never with `= NULL`; supply defaults with `NVL(x, 0)`; and remember that `'a' || NULL` is `'a'` (Oracle treats an empty string as NULL).

**Scope and visibility.** A variable is visible in the block where it is declared and in blocks nested inside it. If an inner block declares the same name, the inner one **hides** the outer one; the outer variable can be reached with a block label (`<<outer>>`).

```plsql
SQL> <<outer>>
  2  DECLARE
  3    x NUMBER := 10;
  4  BEGIN
  5    DECLARE
  6      x NUMBER := 20;
  7    BEGIN
  8      DBMS_OUTPUT.PUT_LINE('inner x = ' || x);
  9      DBMS_OUTPUT.PUT_LINE('outer x = ' || outer.x);
 10    END;
 11    DBMS_OUTPUT.PUT_LINE('x after the inner block = ' || x);
 12  END;
 13  /
inner x = 20
outer x = 10
x after the inner block = 10
```

## 2.6 DML statements in PL/SQL

SQL statements are written inside the executable section exactly as in SQL*Plus, with PL/SQL variables in place of literals. A `SELECT` needs an `INTO` clause to bring the result into variables, and must return **exactly one row**; none raises `NO_DATA_FOUND` and more than one raises `TOO_MANY_ROWS` (Unit 3). For many rows use a cursor (Unit 4).

```plsql
DECLARE
  v_emp  emp%ROWTYPE;                 -- one field for every column of EMP
BEGIN
  SELECT * INTO v_emp FROM emp WHERE empno = 7839;
  DBMS_OUTPUT.PUT_LINE(v_emp.ename || ', ' || v_emp.job || ', ' || v_emp.sal);
END;
/
```
```output
KING, PRESIDENT, 5000

PL/SQL procedure successfully completed.
```

`INSERT`, `UPDATE` and `DELETE` may use variables and expressions. After any DML statement the **implicit cursor** named `SQL` reports what happened:

| Attribute | Meaning |
|---|---|
| `SQL%ROWCOUNT` | Number of rows changed by the last DML statement (or returned by the last single-row SELECT) |
| `SQL%FOUND` | `TRUE` if at least one row was affected |
| `SQL%NOTFOUND` | `TRUE` if no row was affected |

```plsql
DECLARE
  v_new_id emp.empno%TYPE;
  v_pay    NUMBER;
BEGIN
  INSERT INTO emp (empno, ename, job, sal, deptno)
  VALUES (seq_empno.NEXTVAL, 'GURUNG', 'CLERK', 900, 10)
  RETURNING empno INTO v_new_id;                      -- get the generated key back
  DBMS_OUTPUT.PUT_LINE('Hired GURUNG with empno ' || v_new_id);

  UPDATE emp SET sal = sal * 1.10 WHERE deptno = 10;  -- GURUNG is included now: 4 rows
  DBMS_OUTPUT.PUT_LINE(SQL%ROWCOUNT || ' employees updated');

  DELETE FROM emp WHERE empno = 9999;                 -- no such employee
  IF SQL%NOTFOUND THEN
    DBMS_OUTPUT.PUT_LINE('Nobody with empno 9999 to delete');
  END IF;
  ROLLBACK;                                           -- leave the demo data unchanged
END;
/
```
```output
Hired GURUNG with empno 8000
4 employees updated
Nobody with empno 9999 to delete

PL/SQL procedure successfully completed.
```

(The sequence of Unit 1.7 is assumed to be at its first value, 8000. A sequence is **not** rolled back, so running the block again gives 8001.) A second use of `RETURNING` is to see the new value of an update: `UPDATE emp SET sal = sal * 1.1 WHERE empno = 7369 RETURNING sal INTO v_sal;` stores 880 in `v_sal` without a second query.

::: caution Common mistake
`SELECT sal INTO v_sal FROM emp WHERE deptno = 10;` compiles, but at run time it raises `TOO_MANY_ROWS` because department 10 has three employees. A single-row SELECT INTO is for primary-key or aggregate queries only.
:::

## 2.7 Transaction control in PL/SQL

`COMMIT`, `ROLLBACK` and `SAVEPOINT` are PL/SQL statements as well. A transaction starts at the first DML and ends at a COMMIT or ROLLBACK; the block itself is **not** a transaction, so a block may contain several transactions or leave one open for the caller to finish. A DDL statement cannot be written directly in PL/SQL (it needs `EXECUTE IMMEDIATE`), and when it runs it commits.

```plsql
DECLARE
  v_n   PLS_INTEGER;
  v_pay NUMBER;
BEGIN
  UPDATE emp SET sal = sal + 100 WHERE deptno = 20;
  DBMS_OUTPUT.PUT_LINE('Updated: ' || SQL%ROWCOUNT);
  SAVEPOINT after_raise;

  DELETE FROM emp WHERE deptno = 20;
  DBMS_OUTPUT.PUT_LINE('Deleted: ' || SQL%ROWCOUNT);

  ROLLBACK TO after_raise;                        -- undo only the delete
  SELECT COUNT(*), SUM(sal) INTO v_n, v_pay FROM emp WHERE deptno = 20;
  DBMS_OUTPUT.PUT_LINE('Department 20 now has ' || v_n || ' employees, payroll ' || v_pay);
  COMMIT;                                         -- make the raise permanent
END;
/
```
```output
Updated: 5
Deleted: 5
Department 20 now has 5 employees, payroll 11375

PL/SQL procedure successfully completed.
```

Department 20 has five employees paid 10,875 in total, so the raise of 100 each makes 10,875 + 5 × 100 = 11,375. The rollback to the savepoint restores the five deleted rows but keeps the raise. Two further facts: an **unhandled error** in a block does not by itself roll back the whole transaction (only the failed statement is undone), and a failed program called from SQL*Plus leaves the earlier changes pending until you COMMIT or ROLLBACK. For this reason, programs that change data should end with an explicit COMMIT or ROLLBACK decision, and stored procedures usually leave that decision to the caller.

## 2.8 Conditional control

**IF** chooses between paths. Forms:

```plsql
IF cond THEN ... END IF;
IF cond THEN ... ELSE ... END IF;
IF c1 THEN ... ELSIF c2 THEN ... ELSIF c3 THEN ... ELSE ... END IF;   -- note the spelling: ELSIF
```

IF statements can be **nested** inside one another. Conditions are tested top to bottom and the first TRUE branch runs; the rest are skipped.

```plsql
DECLARE
  v_sal   emp.sal%TYPE;
  v_grade VARCHAR2(10);
BEGIN
  SELECT sal INTO v_sal FROM emp WHERE empno = &empno;
  IF    v_sal >= 5000 THEN v_grade := 'Executive';
  ELSIF v_sal >= 2500 THEN v_grade := 'Senior';
  ELSIF v_sal >= 1000 THEN v_grade := 'Junior';
  ELSE                     v_grade := 'Trainee';
  END IF;
  DBMS_OUTPUT.PUT_LINE('Salary ' || v_sal || ' is grade ' || v_grade);
END;
/
```

| Entered empno | Salary | Output |
|---|---|---|
| 7369 (SMITH) | 800 | `Salary 800 is grade Trainee` |
| 7499 (ALLEN) | 1600 | `Salary 1600 is grade Junior` |
| 7566 (JONES) | 2975 | `Salary 2975 is grade Senior` |
| 7839 (KING) | 5000 | `Salary 5000 is grade Executive` |

The order of the tests matters: if `>= 1000` came first, KING would be called Junior.

**The NULL trap.** A condition that evaluates to NULL is not TRUE, so the ELSE branch runs:

```plsql
DECLARE
  v_comm emp.comm%TYPE;
BEGIN
  SELECT comm INTO v_comm FROM emp WHERE ename = '&name';     -- try SMITH (NULL) and TURNER (0)
  IF v_comm > 0 THEN
    DBMS_OUTPUT.PUT_LINE('earns commission');
  ELSE
    DBMS_OUTPUT.PUT_LINE('no commission');       -- also printed for NULL
  END IF;
  IF v_comm IS NULL THEN
    DBMS_OUTPUT.PUT_LINE('not in the commission scheme');
  ELSIF v_comm = 0 THEN
    DBMS_OUTPUT.PUT_LINE('in the scheme, nothing earned this month');
  END IF;
END;
/
```

For SMITH (commission NULL) the output is `no commission` and `not in the commission scheme`. For TURNER (commission 0) it is `no commission` and `in the scheme, nothing earned this month`. The first test cannot tell the two cases apart; the second can.

**CASE** has two forms. The **simple CASE** compares one expression with several values; the **searched CASE** evaluates independent conditions. Both exist as a **statement** (`END CASE;`) and as an **expression** (`END`) that returns a value.

```plsql
DECLARE
  v_job   emp.job%TYPE;
  v_sal   emp.sal%TYPE;
  v_bonus NUMBER(8,2);
BEGIN
  SELECT job, sal INTO v_job, v_sal FROM emp WHERE empno = &empno;
  v_bonus := CASE v_job                              -- simple CASE expression
               WHEN 'CLERK'    THEN 0.05 * v_sal
               WHEN 'SALESMAN' THEN 0.10 * v_sal
               WHEN 'MANAGER'  THEN 0.15 * v_sal
               ELSE                 0.02 * v_sal
             END;
  DBMS_OUTPUT.PUT_LINE(v_job || ' with salary ' || v_sal || ' gets bonus ' || v_bonus);
  CASE                                               -- searched CASE statement
    WHEN v_bonus >= 400 THEN DBMS_OUTPUT.PUT_LINE('large bonus');
    WHEN v_bonus >= 100 THEN DBMS_OUTPUT.PUT_LINE('medium bonus');
    ELSE                     DBMS_OUTPUT.PUT_LINE('small bonus');
  END CASE;
END;
/
```

| Entered empno | Job and salary | Bonus | Output lines |
|---|---|---|---|
| 7499 | SALESMAN, 1600 | 160 | `SALESMAN with salary 1600 gets bonus 160` and `medium bonus` |
| 7788 | ANALYST, 3000 | 60 | `ANALYST with salary 3000 gets bonus 60` and `small bonus` |
| 7566 | MANAGER, 2975 | 446.25 | `MANAGER with salary 2975 gets bonus 446.25` and `large bonus` |

If no WHEN matches in a CASE **statement** and there is no ELSE, Oracle raises `CASE_NOT_FOUND` (ORA-06592); a CASE **expression** without ELSE returns NULL instead. Always write an ELSE.

## 2.9 Repetitive control

A loop repeats statements. PL/SQL has three loop forms plus the exit controls `EXIT`, `EXIT WHEN` and `CONTINUE`.

**Simple (basic) LOOP.** The body repeats until an `EXIT` runs; it always executes at least once, and forgetting the exit gives an endless loop.

```plsql
DECLARE
  n PLS_INTEGER := 1;
  f NUMBER := 1;
BEGIN
  LOOP
    f := f * n;
    EXIT WHEN n = 5;          -- same as IF n = 5 THEN EXIT; END IF;
    n := n + 1;
  END LOOP;
  DBMS_OUTPUT.PUT_LINE('5! = ' || f);
END;
/
```
```output
5! = 120

PL/SQL procedure successfully completed.
```

**WHILE loop.** The condition is tested **before** each pass, so the body may run zero times.

```plsql
DECLARE
  i PLS_INTEGER := 1;
  s PLS_INTEGER := 0;
BEGIN
  WHILE i <= 100 LOOP
    s := s + i;
    i := i + 1;
  END LOOP;
  DBMS_OUTPUT.PUT_LINE('Sum of 1 to 100 = ' || s);
END;
/
```
```output
Sum of 1 to 100 = 5050

PL/SQL procedure successfully completed.
```

**Numeric FOR loop.** The counter is declared **implicitly**, exists only inside the loop, is read-only, and steps by 1 (use `REVERSE` to count down). The two bounds are evaluated once, before the loop starts; if the lower bound is greater than the upper one the body never runs.

```plsql
DECLARE
  v_line VARCHAR2(40);
BEGIN
  FOR i IN 1..5 LOOP
    DBMS_OUTPUT.PUT_LINE('7 x ' || i || ' = ' || 7 * i);
  END LOOP;
  FOR i IN REVERSE 1..5 LOOP
    v_line := v_line || i || ' ';
  END LOOP;
  DBMS_OUTPUT.PUT_LINE('Countdown: ' || TRIM(v_line));
END;
/
```
```output
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
Countdown: 5 4 3 2 1

PL/SQL procedure successfully completed.
```

The loop counter works well with DML. This block fills a table and then totals it (1 + 4 + 9 + 16 + 25 = 55):

```plsql
CREATE TABLE squares (n NUMBER, sq NUMBER);

DECLARE
  v_total NUMBER;
BEGIN
  FOR i IN 1..5 LOOP
    INSERT INTO squares VALUES (i, i * i);
  END LOOP;
  SELECT SUM(sq) INTO v_total FROM squares;
  DBMS_OUTPUT.PUT_LINE('Rows: 5, sum of squares: ' || v_total);
  COMMIT;
END;
/
```
```output
Rows: 5, sum of squares: 55
```

**Nested loops, CONTINUE and labels.** Loops can be placed inside loops. A **label** `<<name>>` before a loop lets `EXIT name` leave an outer loop, and `CONTINUE` (Oracle 11g and later) skips the rest of the current pass.

```plsql
DECLARE
  v_line VARCHAR2(20);
BEGIN
  FOR i IN 1..4 LOOP                       -- a triangle of stars: inner loop runs i times
    v_line := NULL;
    FOR j IN 1..i LOOP
      v_line := v_line || '*';
    END LOOP;
    DBMS_OUTPUT.PUT_LINE(v_line);
  END LOOP;

  v_line := NULL;
  FOR i IN 1..9 LOOP
    CONTINUE WHEN MOD(i, 2) = 0;           -- skip even numbers
    v_line := v_line || i || ' ';
  END LOOP;
  DBMS_OUTPUT.PUT_LINE('Odd numbers: ' || TRIM(v_line));

  <<outer_loop>>
  FOR i IN 1..5 LOOP
    FOR j IN 1..5 LOOP
      IF i * j = 12 THEN
        DBMS_OUTPUT.PUT_LINE('First pair with product 12: i=' || i || ', j=' || j);
        EXIT outer_loop;                   -- leaves BOTH loops
      END IF;
    END LOOP;
  END LOOP outer_loop;
END;
/
```
```output
*
**
***
****
Odd numbers: 1 3 5 7 9
First pair with product 12: i=3, j=4

PL/SQL procedure successfully completed.
```

A plain `EXIT` in the inner loop would leave only the inner loop, so the outer loop would continue with the next `i`. PL/SQL also has `GOTO label`, but it makes programs hard to follow and nothing in this course needs it.

| Loop | Test | Runs at least once? | Use when |
|---|---|---|---|
| Simple LOOP with EXIT WHEN | At the exit statement (anywhere in the body) | Yes | The number of passes is not known and the body must run once |
| WHILE | Before each pass | No | Repeat while a condition holds |
| FOR | Bounds fixed at the start | Only if lower bound ≤ upper bound | The number of passes is known |

## 2.10 Summary and exercises

PL/SQL runs in the Oracle server; the PL/SQL engine executes procedural statements and passes SQL to the SQL executor, so a whole block costs one round trip. A block has optional DECLARE, mandatory BEGIN ... END and optional EXCEPTION sections; anonymous blocks are compiled on each run, named blocks are stored. `DBMS_OUTPUT.PUT_LINE` prints once `SERVEROUTPUT` is on, and `&name` is replaced by SQL*Plus before the block is compiled. `%TYPE` and `%ROWTYPE` anchor variables to the database; NULL makes a condition not TRUE; `SQL%ROWCOUNT` reports the effect of DML; COMMIT, ROLLBACK and SAVEPOINT work as in SQL; IF/ELSIF and CASE select, and LOOP, WHILE and FOR repeat, with EXIT, CONTINUE and labels for control.

1. What is PL/SQL? Give five advantages over using SQL alone.
2. Draw and explain the architecture of PL/SQL.
3. Explain the structure of a PL/SQL block. Which sections are optional? What is the difference between an anonymous and a named block?
4. Why does `DBMS_OUTPUT.PUT_LINE` print nothing in SQL*Plus until `SET SERVEROUTPUT ON` is given?
5. Write a block that reads an employee number with a substitution variable and prints the name, job and annual salary.
6. Explain `%TYPE` and `%ROWTYPE` with an example. Why are they better than writing `NUMBER(7,2)`?
7. What is the value of `NULL = NULL`? Of `TRUE AND NULL`? Of `FALSE AND NULL`? How must a NULL be tested?
8. What is the output of: `BEGIN IF NULL THEN DBMS_OUTPUT.PUT_LINE('A'); ELSE DBMS_OUTPUT.PUT_LINE('B'); END IF; END;`?
9. Explain the three forms of `IF` and the two forms of `CASE` with an example each.
10. Write a block that prints the first ten Fibonacci numbers.
11. Write a block that uses a WHILE loop to find the sum of the digits of 4,725.
12. Explain EXIT, EXIT WHEN, CONTINUE and loop labels. How do you leave two nested loops at once?
13. Write a block that raises the salary of all clerks by 5 percent, prints the number of rows changed, and undoes the change.
14. What does `SQL%ROWCOUNT` return after `UPDATE emp SET sal = sal WHERE deptno = 99;`?

**Answers to the numerical items.** (7) `NULL = NULL` is NULL (unknown); `TRUE AND NULL` is NULL; `FALSE AND NULL` is FALSE; test with `IS NULL`. (8) `B`, since NULL is not TRUE. (10) the terms are 0, 1, 1, 2, 3, 5, 8, 13, 21, 34. (11) the digits sum to $4+7+2+5=18$; a block takes `n MOD 10` and `TRUNC(n/10)` in turn. (13) the four clerks (SMITH, ADAMS, JAMES, MILLER) are updated, so the printed count is 4. (14) 0, because department 99 does not exist.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the structure of a PL/SQL block.**

A block has three sections. The optional **declarative** section starts with DECLARE and defines variables, constants, cursors and user exceptions. The mandatory **executable** section lies between BEGIN and END and holds SQL and procedural statements. The optional **exception** section, introduced by EXCEPTION, holds handlers for errors. A block ends with `END;`. Blocks may be nested. Example: `DECLARE v NUMBER := 5; BEGIN DBMS_OUTPUT.PUT_LINE(v * 2); END;` prints 10. Anonymous blocks have no name and are not stored; procedures, functions, packages and triggers are named blocks stored in the database.

**Q2 (5 marks). Compare the loops of PL/SQL.**

The simple LOOP repeats until an EXIT statement and always executes once. The WHILE loop tests its condition before each pass and may not run at all. The FOR loop declares its counter implicitly, steps by one (backwards with REVERSE) and fixes its bounds when it starts. Example: `FOR i IN 1..5 LOOP DBMS_OUTPUT.PUT_LINE(7 * i); END LOOP;` prints 7, 14, 21, 28 and 35. EXIT WHEN leaves a loop on a condition, CONTINUE skips to the next pass and labels allow an inner statement to leave an outer loop.

**Q3 (10 marks). What is PL/SQL? Describe its architecture and advantages.**

*Introduction.* PL/SQL is Oracle's procedural extension of SQL: block-structured, with variables, control statements, exception handling and subprograms, executed inside the server.

*Architecture.* A block from the client reaches the Oracle server, where the PL/SQL engine runs the procedural statements; each SQL statement is passed to the SQL statement executor, which works on the data, and the result returns to the engine. The whole block crosses the network once.

*Advantages.* (1) Performance: one round trip for many statements, and compiled stored code reused through the shared pool. (2) Integration: the same data types as the database, `%TYPE` and `%ROWTYPE`. (3) Modularity: procedures, functions and packages. (4) Error handling through exceptions. (5) Security: users may be granted EXECUTE on a program without rights on the tables. (6) Portability to every platform that runs Oracle.

*Example.* A block that reads an employee's salary, decides a bonus with CASE and updates the row replaces three client round trips by one.

*Conclusion.* PL/SQL combines SQL's power over data with the control a programming language gives, close to the data.

**Q4 (10 marks). Explain the conditional and repetitive control structures of PL/SQL with examples.**

*Conditional.* IF-THEN runs a part when the condition is TRUE; IF-THEN-ELSE chooses one of two; IF-ELSIF-ELSE chooses among many, and the first TRUE test wins. A condition that is NULL counts as not TRUE. The simple CASE compares one expression with values and the searched CASE evaluates conditions; both may be an expression or a statement, and a CASE statement with no matching WHEN and no ELSE raises CASE_NOT_FOUND. Example: salary 2975 with `IF sal >= 5000 ... ELSIF sal >= 2500` gives 'Senior'.

*Repetitive.* The simple LOOP with EXIT WHEN, for example computing 5! = 120; the WHILE loop, for example summing 1 to 100 to get 5050; the FOR loop for a known count, for example printing 7 x 1 to 7 x 5. Loops may be nested, CONTINUE WHEN MOD(i, 2) = 0 skips even numbers, and `EXIT outer_loop` leaves two loops at once.

*Conclusion.* Together these constructs let a block express any algorithm while working on database rows.
