---
subject: Database Programming
grade: BCA Semester 8 (Elective III)
unit: 7
title: Functions and Packages
hours: 5
area: BCA 453 · Database Programming · Unit 7
---

The word "net pay" means the same thing in the payroll screen, in the monthly report and in the bank transfer file. If each of them calculates it in its own way, sooner or later they disagree. The cure is to write the calculation **once**, inside the database, as a **function**, and to collect related functions, procedures and variables into one named unit, a **package**. This last unit completes the stored-program toolkit of the course.

::: key What this unit gives you
- Functions: syntax, the RETURN statement, calling from PL/SQL and from SQL, and how functions differ from procedures.
- Optimising function execution: DETERMINISTIC, RESULT_CACHE, fewer calls per row.
- Packages: specification and body, public and private items, overloading.
- Creating, extending, instantiating and initialising a package, and a lab checklist for the whole course.
:::

## 7.1 Creating and invoking functions

A **function** is a stored named block that **returns one value**. It is used inside an expression, not as a separate statement.

```plsql
CREATE [OR REPLACE] FUNCTION function_name
  [(parameter1 [IN] datatype [:= default], ...)]
  RETURN return_datatype
IS | AS
  -- declarations
BEGIN
  -- statements, including at least one RETURN expression;
  RETURN value;
[EXCEPTION
  -- handlers: every path must also end in RETURN or raise an exception]
END [function_name];
/
```

The return type has **no size** (`RETURN VARCHAR2`). A function should end through a `RETURN` on **every** path; a function that reaches `END` without one raises `ORA-06503: PL/SQL: Function returned without value`. Parameters are normally IN. Although OUT parameters are legal, they make a function hard to use and are not allowed when the function is called from SQL.

```plsql
CREATE OR REPLACE FUNCTION net_pay (p_empno IN emp.empno%TYPE)
  RETURN NUMBER
IS
  v_sal  emp.sal%TYPE;
  v_comm emp.comm%TYPE;
BEGIN
  SELECT sal, comm INTO v_sal, v_comm FROM emp WHERE empno = p_empno;
  RETURN v_sal + NVL(v_comm, 0);                  -- a NULL commission counts as 0
EXCEPTION
  WHEN NO_DATA_FOUND THEN
    RETURN NULL;                                  -- the caller can test IS NULL
END net_pay;
/
```

**Calling a function.** In four ways:

```plsql
-- 1. in a PL/SQL expression
DECLARE
  v_pay NUMBER;
BEGIN
  v_pay := net_pay(7499);
  DBMS_OUTPUT.PUT_LINE('ALLEN gets ' || v_pay);
END;
/

-- 2. directly in a SELECT or WHERE clause
SELECT ename, net_pay(empno) AS pay FROM emp WHERE deptno = 30 AND net_pay(empno) > 1700 ORDER BY ename;

-- 3. from DUAL or a SQL*Plus bind variable
SELECT net_pay(7369) FROM dual;
VARIABLE b NUMBER
EXEC :b := net_pay(7654)
```

| Call | Result |
|---|---|
| `net_pay(7499)` (ALLEN: salary 1600, commission 300) | 1900 |
| `net_pay(7369)` (SMITH: salary 800, commission NULL) | 800 |
| `net_pay(7654)` (MARTIN: salary 1250, commission 1400) | 2650 |
| `net_pay(9999)` | NULL |

The SELECT of call 2 returns the department 30 employees whose net pay is above 1700, in name order:

```plsql
ENAME             PAY
---------- ----------
ALLEN            1900
BLAKE            2850
MARTIN           2650
WARD             1750
```

(TURNER earns 1500 + 0 and JAMES 950, so they are filtered out.) Notice that a function with a `SELECT` inside, called from a `SELECT`, runs a query **once for every row**; the next section returns to this cost.

**A function with logic and no table: a tax calculation.** The slabs below are an *illustrative teaching model* (not the current Nepal rates, which change every budget): 1 percent on the first 500,000, 10 percent on the next 200,000, 20 percent on the next 300,000 and 30 percent on anything above 1,000,000.

```plsql
CREATE OR REPLACE FUNCTION annual_tax (p_income IN NUMBER) RETURN NUMBER
  DETERMINISTIC                                   -- same input always gives the same output
IS
  v_tax NUMBER := 0;
BEGIN
  IF p_income IS NULL OR p_income < 0 THEN
    RETURN NULL;
  END IF;
  v_tax := 0.01 * LEAST(p_income, 500000);
  IF p_income > 500000  THEN v_tax := v_tax + 0.10 * (LEAST(p_income, 700000)  - 500000); END IF;
  IF p_income > 700000  THEN v_tax := v_tax + 0.20 * (LEAST(p_income, 1000000) - 700000); END IF;
  IF p_income > 1000000 THEN v_tax := v_tax + 0.30 * (p_income - 1000000); END IF;
  RETURN v_tax;
END annual_tax;
/
```

| Income | Working | Tax |
|---|---|---|
| 400,000 | 1% of 400,000 | 4,000 |
| 650,000 | 5,000 + 10% of 150,000 | 20,000 |
| 1,200,000 | 5,000 + 20,000 + 60,000 + 30% of 200,000 | 145,000 |

`SELECT ename, annual_tax(sal * 12) FROM emp` would apply it to every employee (reading the salary as a monthly amount in rupees). A **recursive function** calls itself; it needs a stopping case:

```plsql
CREATE OR REPLACE FUNCTION fact (n IN PLS_INTEGER) RETURN NUMBER IS
BEGIN
  IF n <= 1 THEN
    RETURN 1;                  -- stopping case
  END IF;
  RETURN n * fact(n - 1);
END;
/
-- SELECT fact(5), fact(10) FROM dual;   gives 120 and 3628800
```

**Function or procedure?**

| | Procedure | Function |
|---|---|---|
| Called | As a statement | Inside an expression |
| Returns | Nothing directly; OUT / IN OUT parameters | **Exactly one** value, through RETURN |
| Callable from SQL | No | Yes, if it follows the purity rules below |
| Typical use | An action: insert, update, report | A calculation or lookup |

**Rules for functions called from SQL.** The function must be a stored function (or package function), use only IN parameters and SQL-compatible types (BOOLEAN and records are not allowed), and, when called from a `SELECT`, must not perform DML, `COMMIT` or `ROLLBACK` on tables. A function that changes data can be called only from PL/SQL.

## 7.2 Optimising function execution

A function used in a SQL statement is run once per row examined. If a table has a million rows, the function runs a million times, and each call switches from the SQL engine to the PL/SQL engine and back. Ways to keep the cost down:

| Technique | How and why |
|---|---|
| **Call it less** | Put the function in the `SELECT` list rather than the `WHERE` clause, or filter with plain SQL first, so that it runs only for the rows you keep |
| **`DETERMINISTIC`** | Promises the same result for the same input, so Oracle may reuse results within a statement and the function can be used in a **function-based index**: `CREATE INDEX i ON emp(annual_tax(sal));` |
| **`RESULT_CACHE`** (11g and later) | Oracle stores results in the SGA, shared by all sessions, and invalidates them when the tables used change: `FUNCTION country_name(p_code VARCHAR2) RETURN VARCHAR2 RESULT_CACHE` |
| **Scalar subquery caching** | `SELECT (SELECT net_pay(empno) FROM dual) ...` lets Oracle cache results for repeated inputs |
| **Replace by SQL** | If the logic is one `CASE` or arithmetic expression, write it inline; no engine switch at all |
| **`PRAGMA UDF`** (12c) | Compiles a function meant mainly for SQL so that calls from SQL are cheaper |
| **Avoid SQL inside the function** | A lookup of a small table per row is better done with a join |
| **Use `PLS_INTEGER`** | For counters and loop variables inside the function |
| **Measure** | `SET TIMING ON`, `DBMS_UTILITY.GET_TIME`, or SQL trace, before and after |
| **Pass collections by `NOCOPY`** | Avoids copying a large IN OUT collection (a hint) |

The idea behind a result cache is **memoisation**: remember answers already computed. The Python program below counts how many calls a recursive Fibonacci function makes with and without a remembered-results table. The same arithmetic applies to PL/SQL recursion, and shows why caching a function can change the cost by orders of magnitude.

```python
calls = 0
def fib(n):
    global calls
    calls += 1
    return n if n < 2 else fib(n - 1) + fib(n - 2)

memo, mcalls = {}, 0
def fib_cached(n):
    global mcalls
    mcalls += 1
    if n in memo: return memo[n]
    memo[n] = n if n < 2 else fib_cached(n - 1) + fib_cached(n - 2)
    return memo[n]

print("fib(25) =", fib(25), "after", calls, "calls")
print("fib_cached(25) =", fib_cached(25), "after", mcalls, "calls")
print("ratio: %.0f times fewer calls" % (calls / mcalls))
```
```output
fib(25) = 75025 after 242785 calls
fib_cached(25) = 75025 after 49 calls
ratio: 4955 times fewer calls
```
A cache is only correct when the function is truly a function of its inputs. A function that reads `SYSDATE` or a table that changes must **not** be marked `DETERMINISTIC`; `RESULT_CACHE` handles table changes itself by tracking the tables the function reads (with a `RELIES_ON` clause in older releases).

## 7.3 Packages

A **package** is a stored schema object that groups logically related **types, variables, constants, cursors, procedures and functions** under one name. It has two parts:

| Part | Contains | Visible to |
|---|---|---|
| **Specification** (spec, "header") | Declarations only: the *public interface* | Every user with `EXECUTE` on the package |
| **Body** | The code of the subprograms, plus private items not in the spec | Only the package itself |

```svgfig label="7.1" caption="A package. Callers see only the specification; the body holds the code and the private items."
f = Fig(640, 250)
f.box(10, 10, 130, 230, "Callers\nSQL*Plus,\nblocks,\napplications", fill=SOFT, stroke=SLATE, size=10)
f.box(190, 10, 280, 80, "", fill=SAND, stroke=AMBER)
f.text(330, 26, "PACKAGE SPECIFICATION (public)", size=10, anchor="middle", color=AMBER)
f.text(330, 48, "c_max_pct   CONSTANT NUMBER", size=9.5, anchor="middle", color=SLATE)
f.text(330, 64, "PROCEDURE raise_salary(...)", size=9.5, anchor="middle", color=SLATE)
f.text(330, 80, "FUNCTION net_pay(...)", size=9.5, anchor="middle", color=SLATE)
f.box(190, 120, 280, 120, "", fill=BLUE, stroke=NAVY)
f.text(330, 136, "PACKAGE BODY (hidden)", size=10, anchor="middle", color=NAVY)
f.text(330, 158, "code of raise_salary and net_pay", size=9.5, anchor="middle", color=SLATE)
f.text(330, 176, "private function valid_pct(...)", size=9.5, anchor="middle", color=SLATE)
f.text(330, 194, "private variable g_raise_count", size=9.5, anchor="middle", color=SLATE)
f.text(330, 222, "initialisation block (runs once)", size=9.5, anchor="middle", color=SLATE)
f.arrow([(140, 50), (190, 50)], color=NAVY, label="call", lpos=(165, 40))
f.arrow([(330, 90), (330, 120)], color=TEAL, dash=True)
```

**Advantages of packages**

1. **Modularity and encapsulation**: related code lives together and private items are hidden, so users depend only on the interface.
2. **Easier maintenance**: changing the body does not invalidate programs that call the package; only a change to the spec does.
3. **Performance**: the whole package is loaded into memory when first used, so later calls need no disk access.
4. **Persistent state**: a package variable keeps its value for the whole session (Section 7.6).
5. **Overloading**: several subprograms may share one name if their parameters differ.
6. **Security**: grant `EXECUTE` on the package instead of rights on its tables.

Oracle ships many packages: `DBMS_OUTPUT` (the printing used throughout), `DBMS_RANDOM`, `DBMS_UTILITY`, `UTL_FILE` (read and write operating-system files), `DBMS_SQL` and `EXECUTE IMMEDIATE` (dynamic SQL), `DBMS_SCHEDULER` (jobs) and `UTL_MAIL`.

## 7.4 Creating a package

```plsql
CREATE OR REPLACE PACKAGE emp_pkg IS
  c_max_pct       CONSTANT NUMBER := 50;               -- public constant
  g_raise_count   PLS_INTEGER := 0;                    -- public variable (session state)

  PROCEDURE raise_salary (p_empno IN emp.empno%TYPE, p_pct IN NUMBER DEFAULT 10);
  FUNCTION  net_pay      (p_empno IN emp.empno%TYPE) RETURN NUMBER;
  FUNCTION  dept_payroll (p_dno   IN dept.deptno%TYPE) RETURN NUMBER;
END emp_pkg;
/

CREATE OR REPLACE PACKAGE BODY emp_pkg IS

  FUNCTION valid_pct (p_pct NUMBER) RETURN BOOLEAN IS        -- PRIVATE: not in the spec
  BEGIN
    RETURN p_pct BETWEEN 0 AND c_max_pct;
  END valid_pct;

  PROCEDURE raise_salary (p_empno IN emp.empno%TYPE, p_pct IN NUMBER DEFAULT 10) IS
  BEGIN
    IF NOT valid_pct(p_pct) THEN
      RAISE_APPLICATION_ERROR(-20006,
        'A raise of ' || p_pct || ' percent is outside 0 to ' || c_max_pct);
    END IF;
    UPDATE emp SET sal = sal * (1 + p_pct / 100) WHERE empno = p_empno;
    IF SQL%NOTFOUND THEN
      RAISE_APPLICATION_ERROR(-20003, 'Employee ' || p_empno || ' not found');
    END IF;
    g_raise_count := g_raise_count + 1;
  END raise_salary;

  FUNCTION net_pay (p_empno IN emp.empno%TYPE) RETURN NUMBER IS
    v_pay NUMBER;
  BEGIN
    SELECT sal + NVL(comm, 0) INTO v_pay FROM emp WHERE empno = p_empno;
    RETURN v_pay;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN NULL;
  END net_pay;

  FUNCTION dept_payroll (p_dno IN dept.deptno%TYPE) RETURN NUMBER IS
    v_total NUMBER;
  BEGIN
    SELECT NVL(SUM(sal), 0) INTO v_total FROM emp WHERE deptno = p_dno;
    RETURN v_total;
  END dept_payroll;

END emp_pkg;
/
```

Rules. The spec must be created **before** the body. A subprogram declared in the spec **must** be defined in the body with a matching header, and the body may define extra private subprograms. A private subprogram must be defined **before** it is used in the body, or declared ahead with a *forward declaration* (the header followed by a semicolon). Items are used with the dot form `package.item`.

```plsql
SQL> EXEC emp_pkg.raise_salary(7369, 25)
SQL> EXEC emp_pkg.raise_salary(7499)
SQL> EXEC DBMS_OUTPUT.PUT_LINE('Raises this session: ' || emp_pkg.g_raise_count)
Raises this session: 2
SQL> EXEC DBMS_OUTPUT.PUT_LINE('Net pay of ALLEN: ' || emp_pkg.net_pay(7499))
Net pay of ALLEN: 2060
SQL> EXEC DBMS_OUTPUT.PUT_LINE('Payroll of department 30: ' || emp_pkg.dept_payroll(30))
Payroll of department 30: 9560
SQL> EXEC emp_pkg.raise_salary(7788, 80)
BEGIN emp_pkg.raise_salary(7788, 80); END;
*
ERROR at line 1:
ORA-20006: A raise of 80 percent is outside 0 to 50
ORA-06512: at "SCOTT.EMP_PKG", line 11
ORA-06512: at line 1
```

Working: the first two calls raise SMITH from 800 to 1000 and ALLEN from 1600 to 1760, so the counter reads 2. ALLEN's net pay is then 1760 + 300 = 2060 (salary plus commission), and department 30, which paid 9,400, now pays 9,400 + 160 = 9,560. The call with 80 percent is rejected by the private function `valid_pct`, which no caller can reach directly; trying `emp_pkg.valid_pct(5)` gives `PLS-00302: component 'VALID_PCT' must be declared`.

## 7.5 Extending a package

A package grows by **editing and recompiling** its spec and body. Two additions show the usual cases. First an **overloaded** function: a second `net_pay` that takes a **name** instead of a number. Overloading requires that the parameter lists differ in number, order or type family (NUMBER against VARCHAR2 is a different family). Second, a new function `top_earner`.

```plsql
-- the spec gets two new declarations (add them before END emp_pkg;)
  FUNCTION net_pay    (p_name IN emp.ename%TYPE) RETURN NUMBER;     -- overload
  FUNCTION top_earner (p_dno  IN dept.deptno%TYPE) RETURN VARCHAR2;

-- the body gets their code (add them before END emp_pkg;)
  FUNCTION net_pay (p_name IN emp.ename%TYPE) RETURN NUMBER IS
    v_pay NUMBER;
  BEGIN
    SELECT sal + NVL(comm, 0) INTO v_pay FROM emp WHERE ename = UPPER(p_name);
    RETURN v_pay;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN NULL;
  END net_pay;

  FUNCTION top_earner (p_dno IN dept.deptno%TYPE) RETURN VARCHAR2 IS
    v_name emp.ename%TYPE;
  BEGIN
    SELECT ename INTO v_name FROM emp
    WHERE  deptno = p_dno AND sal = (SELECT MAX(sal) FROM emp WHERE deptno = p_dno);
    RETURN v_name;
  EXCEPTION
    WHEN NO_DATA_FOUND THEN RETURN 'nobody';
    WHEN TOO_MANY_ROWS THEN RETURN 'tie';
  END top_earner;
```

```plsql
SQL> SELECT emp_pkg.net_pay(7654) AS by_number, emp_pkg.net_pay('martin') AS by_name FROM dual;

 BY_NUMBER    BY_NAME
---------- ----------
      2650       2650

SQL> SELECT emp_pkg.top_earner(10) AS d10, emp_pkg.top_earner(20) AS d20, emp_pkg.top_earner(40) AS d40 FROM dual;

D10        D20        D40
---------- ---------- ----------
KING       tie        nobody
```

Department 20 returns `tie` because SCOTT and FORD both earn 3000 (which raises `TOO_MANY_ROWS`), and department 40 has no employees. The overload is chosen at compile time from the type of the actual argument.

**Effect of a change on the programs that use the package.** Oracle tracks dependencies:

| Change | Effect on dependent programs |
|---|---|
| Body only (the code of an existing subprogram) | **No** invalidation; callers keep working |
| Specification (a new subprogram, a changed header) | Dependent programs become `INVALID` and are recompiled automatically at their next call (`ALTER PACKAGE emp_pkg COMPILE;` does the package, `COMPILE BODY` only the body) |

This is the main maintenance benefit of packages: if the interface is stable, the implementation can be improved at will. In the lab, always create or alter the spec first, check it with `SHOW ERRORS`, then the body.

## 7.6 Package instantiation and initialisation

A package is **instantiated** (loaded into the session's memory, with its variables created) the **first time** any of its items is referenced in a session. **Public and private variables then keep their values for the whole session**, across calls and across transactions, and each session has **its own copy**. This is **persistent state**. (The `g_raise_count` of Section 7.4 behaves this way.)

An **initialisation block** is an optional `BEGIN ... END` at the end of the package body, after all subprograms. It runs **once per session**, when the package is first referenced, to set up variables.

```plsql
CREATE OR REPLACE PACKAGE counter_pkg IS
  PROCEDURE bump;
  FUNCTION  current_value RETURN NUMBER;
END counter_pkg;
/

CREATE OR REPLACE PACKAGE BODY counter_pkg IS
  g_count NUMBER;                              -- private package variable

  PROCEDURE bump IS BEGIN g_count := g_count + 1; END bump;
  FUNCTION current_value RETURN NUMBER IS BEGIN RETURN g_count; END current_value;

BEGIN                                          -- initialisation block: once per session
  g_count := 100;
  DBMS_OUTPUT.PUT_LINE('counter_pkg initialised');
END counter_pkg;
/
```

| Step | Session A | Session B (a second user, at the same time) |
|---|---|---|
| 1 | `EXEC counter_pkg.bump` prints `counter_pkg initialised`; the counter becomes 101 | |
| 2 | `EXEC counter_pkg.bump` twice more: 102, 103 | `EXEC counter_pkg.bump` prints `counter_pkg initialised`; its own counter becomes 101 |
| 3 | `SELECT counter_pkg.current_value FROM dual;` gives **103** | `SELECT counter_pkg.current_value FROM dual;` gives **101** |
| 4 | `COMMIT` or `ROLLBACK`: the value is **unchanged** (package state is not transactional) | |
| 5 | The package is recompiled (`ALTER PACKAGE ... COMPILE`): the next call in session A fails once with `ORA-04068: existing state of packages has been discarded`; the call after that re-initialises the counter to 100 | |

The initialisation message appears **once for each session**, not once for each call, and the two sessions never see each other's counter. Package state is therefore useful for caches, session settings and counters, but it must not be used for data that several sessions must share (use a table for that). `PRAGMA SERIALLY_REUSABLE` makes the state last only for one call, which saves memory in large web applications.

**Dictionary views** for packages: `USER_OBJECTS` (types `PACKAGE` and `PACKAGE BODY`, with `STATUS`), `USER_SOURCE` (the code of each part) and `USER_ERRORS`. `DESCRIBE emp_pkg` shows the public interface only. `DROP PACKAGE emp_pkg;` removes both parts; `DROP PACKAGE BODY emp_pkg;` only the body.

| | Standalone procedure or function | Package |
|---|---|---|
| Grouping | One program, one object | Many related items, one object |
| Private items | No | Yes, in the body |
| Persistent variables | No | Yes (per session) |
| Overloading | No | Yes |
| Change impact | Callers invalidated when the header changes | Callers invalidated only when the **spec** changes |
| Loading | Each program loaded when called | Whole package loaded at first use |

## 7.7 Laboratory checklist for the course

The TU outline gives 3 practical hours a week. Use this list on Oracle XE (free) or any Oracle 11g or later database; keep each answer as a `.sql` script and run it with `@`.

| Lab | Unit | Task |
|---|---|---|
| 1 | 1 | Create the EMP and DEPT tables with constraints; practise DESCRIBE, LIST, CHANGE, APPEND, INPUT, DEL, CLEAR BUFFER; save and run a script with `&` values |
| 2 | 1 | Joins and subqueries on EMP and DEPT (the twelve queries of the Unit 1 exercises) |
| 3 | 2 | Blocks with `DBMS_OUTPUT`: arithmetic, `%TYPE`, `%ROWTYPE`; read an employee with a substitution variable |
| 4 | 2 | IF, CASE and the three loops: grade by salary, bonus by job, factorial, Fibonacci, prime test, digit sum |
| 5 | 2 | DML with `SQL%ROWCOUNT`, savepoints and rollback |
| 6 | 3 | Handle `NO_DATA_FOUND`, `TOO_MANY_ROWS`, `ZERO_DIVIDE`, `DUP_VAL_ON_INDEX`; a user-defined exception; `RAISE_APPLICATION_ERROR`; `EXCEPTION_INIT` for ORA-02292 |
| 7 | 4 | Cursor with simple, WHILE and FOR loops; parameterised cursor; nested cursors for a department report; `FOR UPDATE` with `WHERE CURRENT OF` |
| 8 | 5 | Triggers: BEFORE INSERT key and name, salary audit table, no-pay-cut rule, Saturday rule, INSTEAD OF on a join view |
| 9 | 6 | Record types and nested records; procedures with IN, OUT and IN OUT parameters (`raise_salary`, `get_emp`, `dept_stats`, `hire_employee`) |
| 10 | 7 | Functions (`net_pay`, `annual_tax`, `fact`) and the package `emp_pkg` with overloading and an initialisation block |

**A mini-project** that uses everything: a student result system with tables `student`, `subject` and `marks`; a package `result_pkg` with a function `grade(p_marks)`, a procedure `enter_marks` that validates the range 0 to 100 with `RAISE_APPLICATION_ERROR`, a cursor-based procedure that prints each student's total and grade, an audit trigger on `marks`, and an INSTEAD OF trigger on a view that joins the three tables.

## 7.8 Summary and exercises

A function is a stored block that returns one value with RETURN and is called inside expressions, including SQL if it is pure; a procedure is called as a statement. Speed comes from calling functions less, marking them `DETERMINISTIC`, using `RESULT_CACHE` and replacing them with plain SQL where possible. A package has a **specification** (public declarations) and a **body** (code and private items); it supports overloading, persistent per-session state and an initialisation block, and a change to the body does not invalidate callers while a change to the spec does.

1. What is a function? Write the syntax of CREATE FUNCTION and explain each part.
2. Differentiate a procedure from a function.
3. Write a function `grade(p_marks)` that returns 'Distinction' for 80 or more, 'First' for 60 to 79, 'Second' for 45 to 59, 'Pass' for 32 to 44 and 'Fail' below 32. Call it from SQL.
4. In how many ways can a function be called? Which restrictions apply to a function called from a SELECT?
5. Write a recursive function that returns the n-th Fibonacci number.
6. Why can calling a function in the WHERE clause of a large query be slow? List five ways to optimise it.
7. What do `DETERMINISTIC` and `RESULT_CACHE` mean? When must they not be used?
8. What is a package? Explain the specification and the body and the advantages of packages.
9. Write a package `math_pkg` with a function `square`, a function `cube` and a procedure that prints both, showing the spec and body.
10. What is overloading? Show an overloaded package function.
11. How does Oracle react when only the package body is changed, and when the specification is changed?
12. Explain package instantiation and initialisation. What is persistent package state, and why do two sessions see different values?
13. What is the value of `annual_tax(650000)` with the slabs of Section 7.1? What does `fib_cached(25)` save compared with `fib(25)`?

**Answers to the numerical items.** (13) $0.01\times500000=5000$ plus $0.10\times(650000-500000)=15000$ gives **20,000**. The plain recursive Fibonacci made 242,785 calls for `fib(25)`, the cached one 49, about 4,955 times fewer. (3) the boundaries are `>= 80`, `>= 60`, `>= 45`, `>= 32`, tested from the top in an IF-ELSIF chain, so marks 79, 59 and 44 give First, Second and Pass; NULL marks should return NULL. (9) `square(n)` returns `n * n`, so 7 gives 49 and `cube(3)` gives 27.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Differentiate between a procedure and a function.**

A procedure is called as a statement and performs an action; it may return values through OUT and IN OUT parameters but has no return value of its own. A function is called inside an expression, must contain RETURN and returns exactly one value; with only IN parameters and no DML it can also be called from a SELECT. Procedure header: `CREATE PROCEDURE raise_salary(p_empno IN NUMBER)`; function header: `CREATE FUNCTION net_pay(p_empno IN NUMBER) RETURN NUMBER`. Use a procedure for an operation and a function for a calculation or lookup.

**Q2 (5 marks). Explain the advantages of packages.**

A package groups related procedures, functions, variables and types in one named object with a public specification and a hidden body. Advantages: modularity and encapsulation, because private items are hidden; easier maintenance, because a change to the body does not invalidate callers; better performance, because the whole package is loaded into memory at first use; persistent session state for variables; overloading of subprograms; and security through `GRANT EXECUTE` on the package alone.

**Q3 (10 marks). Explain how a package is created, with specification, body and an example.**

*Introduction.* A package is a schema object of two parts, created in the order spec then body.

*Specification.* `CREATE OR REPLACE PACKAGE emp_pkg IS c_max_pct CONSTANT NUMBER := 50; PROCEDURE raise_salary(p_empno IN emp.empno%TYPE, p_pct IN NUMBER DEFAULT 10); FUNCTION net_pay(p_empno IN emp.empno%TYPE) RETURN NUMBER; END emp_pkg;` declares what users may call.

*Body.* `CREATE OR REPLACE PACKAGE BODY emp_pkg IS ... END emp_pkg;` implements every declared subprogram with a matching header and may add private items such as `valid_pct`.

*Use.* `EXEC emp_pkg.raise_salary(7369, 25);` raises SMITH from 800 to 1000, and `emp_pkg.net_pay(7654)` returns 2650. A raise of 80 percent is rejected with ORA-20006.

*Extension.* New subprograms or overloads are added to both parts and recompiled.

*Conclusion.* Packages give structured, reusable and secure database programs.

**Q4 (10 marks). Explain package instantiation, initialisation and persistent state with an example.**

*Instantiation.* The first reference to any item of a package in a session loads it into memory and creates its variables, one copy per session.

*Initialisation.* An optional block `BEGIN ... END package_name;` at the end of the body runs once per session at that moment, to set initial values.

*Example.* In `counter_pkg` the initialisation block sets `g_count := 100` and prints a message. Session A calls `bump` three times and reads 103; session B, started separately, bumps once and reads 101, and both saw the message once.

*Persistent state.* Variables keep values between calls and across COMMIT or ROLLBACK for the whole session, but recompiling the package discards the state (ORA-04068 on the next call). Data that sessions must share must be kept in tables.

*Conclusion.* Instantiation and initialisation give each session its own configured copy of the package, useful for counters, caches and settings.
