---
subject: Database Programming
grade: BCA Semester 8 (Elective III)
unit: 5
title: Database Triggers
hours: 5
area: BCA 453 · Database Programming · Unit 5
---

Someone raises a salary at 11 p.m. on a Friday and nobody can later say who, when or from what value. A constraint cannot answer that; a programmer cannot rely on every application remembering to write a log. A **trigger** solves it at the source: a PL/SQL block stored with the table that Oracle runs **automatically** whenever a row is inserted, updated or deleted, whatever program made the change.

::: key What this unit gives you
- What a trigger is, its parts, its types (BEFORE, AFTER, INSTEAD OF; row and statement) and the order in which they fire.
- `:OLD` and `:NEW`, the `WHEN` clause and the predicates `INSERTING`, `UPDATING` and `DELETING`.
- Worked triggers for key generation, auditing, validation and business hours, and INSTEAD OF triggers for views.
- The mutating-table error, restrictions, and managing triggers with ENABLE, DISABLE and DROP.
:::

## 5.1 What a trigger is and why use one

A **database trigger** is a named PL/SQL block, stored in the database and associated with a table, a view, a schema or the database. It is **fired** by an event; unlike a procedure it is never called by name. Typical uses:

| Use | Example |
|---|---|
| **Auditing** | Record old and new salary, user and time for every change |
| **Derived values** | Fill a key from a sequence, set a default date, convert a name to capitals |
| **Validation** that a constraint cannot express | Salary may never be reduced; no changes on a holiday |
| **Security** | Allow changes only in business hours or from certain users |
| **Maintaining summary data** | Keep a department payroll table in step with EMP |
| **Making a complex view updatable** | INSTEAD OF triggers (Section 5.5) |

Triggers are powerful but have costs: they are invisible to the application programmer, they add work to every statement, and a chain of triggers is hard to debug. A rule that **can** be written as a constraint (NOT NULL, CHECK, foreign key) **should** be.

**Classification**

| Basis | Kinds |
|---|---|
| **Timing** | `BEFORE`, `AFTER`, `INSTEAD OF` (views only) |
| **Event** | `INSERT`, `UPDATE [OF columns]`, `DELETE`; a trigger may name several joined by `OR` |
| **Level** | **Statement** (fires once per statement, the default) or **row** (`FOR EACH ROW`, once per affected row) |
| **Object** | Table, view, schema (DDL events such as `CREATE`, `DROP`) or database (`LOGON`, `STARTUP`) |

## 5.2 Syntax, :OLD and :NEW, and the order of firing

```plsql
CREATE [OR REPLACE] TRIGGER trigger_name
  {BEFORE | AFTER | INSTEAD OF}
  {INSERT | DELETE | UPDATE [OF column, ...]} [OR ...]
  ON table_or_view
  [FOR EACH ROW]
  [WHEN (condition)]
DECLARE
  ... local declarations (optional)
BEGIN
  ... statements
EXCEPTION
  ... handlers (optional)
END;
/
```

Inside a **row** trigger, two pseudo-records hold the row's values:

| Event | `:OLD` | `:NEW` |
|---|---|---|
| `INSERT` | All fields NULL | The row being inserted |
| `UPDATE` | The row before the change | The row after the change |
| `DELETE` | The row being deleted | All fields NULL |

`:NEW` can be **assigned** in a BEFORE row trigger (to change what is stored) but not in an AFTER trigger. They are written with a colon in the trigger body and **without** it inside the `WHEN` clause, which restricts a row trigger to the rows where the condition is true. In a trigger that serves several events, the boolean predicates `INSERTING`, `UPDATING`, `UPDATING('SAL')` and `DELETING` tell which one fired it.

**Order of firing.** For one DML statement that affects several rows, Oracle fires, in this order:

1. the **BEFORE statement** triggers (once);
2. for **each row**: the BEFORE row triggers, then the row is changed, then the AFTER row triggers;
3. the **AFTER statement** triggers (once).

```svgfig label="5.1" caption="Firing order of triggers for one DML statement that changes several rows."
f = Fig(640, 190)
f.box(10, 70, 110, 50, "BEFORE\nstatement\ntrigger", fill=SAND, stroke=AMBER, size=10)
f.box(155, 30, 120, 40, "BEFORE row\ntrigger", fill=BLUE, stroke=NAVY, size=10)
f.box(155, 80, 120, 40, "Row is changed", fill=SOFT, stroke=SLATE, size=10)
f.box(155, 130, 120, 40, "AFTER row\ntrigger", fill=BLUE, stroke=NAVY, size=10)
f.box(390, 70, 110, 50, "AFTER\nstatement\ntrigger", fill=SAND, stroke=AMBER, size=10)
f.arrow([(120, 95), (155, 50)], color=NAVY)
f.arrow([(215, 70), (215, 80)], color=NAVY)
f.arrow([(215, 120), (215, 130)], color=NAVY)
f.arrow([(275, 150), (300, 150), (300, 50), (275, 50)], color=SLATE, dash=True, label="next row", lpos=(338, 100))
f.arrow([(275, 158), (345, 158), (390, 112)], color=NAVY, label="no rows left", lpos=(330, 175))
f.text(565, 40, "A statement that\nchanges 3 rows fires\nrow triggers 3 times,\nstatement triggers once.", size=9, anchor="middle", color=SLATE)
```

## 5.3 Statement-level triggers

A trigger without `FOR EACH ROW` runs **once per statement**, even if the statement changes no row or a thousand rows. It cannot use `:OLD` or `:NEW`. It suits rules about **when or who**, not about values.

```plsql
CREATE OR REPLACE TRIGGER trg_no_saturday
  BEFORE INSERT OR UPDATE OR DELETE ON emp
BEGIN
  IF TO_CHAR(SYSDATE, 'DY', 'NLS_DATE_LANGUAGE=ENGLISH') = 'SAT' THEN
    RAISE_APPLICATION_ERROR(-20010, 'Changes to EMP are not allowed on Saturday');
  END IF;
END;
/
```

Saturday is Nepal's weekly holiday. The block raises an application error, and an error in a BEFORE trigger stops the statement and undoes its work. Trying an update on a Saturday gives:

```plsql
SQL> UPDATE emp SET sal = sal + 1 WHERE empno = 7369;
UPDATE emp SET sal = sal + 1 WHERE empno = 7369
       *
ERROR at line 1:
ORA-20010: Changes to EMP are not allowed on Saturday
ORA-06512: at "SCOTT.TRG_NO_SATURDAY", line 3
ORA-04088: error during execution of trigger 'SCOTT.TRG_NO_SATURDAY'
```

(The message lines show the trigger name; `ORA-04088` is always added when a trigger fails.) On other days the statement runs as normal. The same trigger can be written to allow only office hours with `TO_CHAR(SYSDATE, 'HH24') NOT BETWEEN '10' AND '16'`.

## 5.4 Row-level triggers

A trigger with `FOR EACH ROW` runs **once for every affected row** and can read and, in BEFORE triggers, change the row through `:OLD` and `:NEW`.

**Example 1: BEFORE INSERT to fill derived values.**

```plsql
CREATE OR REPLACE TRIGGER trg_emp_bi
  BEFORE INSERT ON emp
  FOR EACH ROW
BEGIN
  IF :NEW.empno IS NULL THEN
    :NEW.empno := seq_empno.NEXTVAL;            -- key from the sequence of Unit 1
  END IF;
  :NEW.ename    := UPPER(:NEW.ename);          -- store names in capitals
  :NEW.hiredate := NVL(:NEW.hiredate, SYSDATE);
END;
/
```

```plsql
SQL> INSERT INTO emp (ename, job, sal, deptno) VALUES ('gurung', 'CLERK', 900, 10);
1 row created.
SQL> SELECT empno, ename FROM emp WHERE job = 'CLERK' AND deptno = 10 AND sal = 900;

     EMPNO ENAME
---------- ----------
      8000 GURUNG
```

The application did not supply a key, a capital name or a hire date; the trigger did. (Assuming `seq_empno` is at its first value.)

**Example 2: AFTER UPDATE to audit salary changes.** The `OF sal` and `WHEN` clauses restrict the trigger to real salary changes.

```plsql
CREATE TABLE emp_audit (
  empno NUMBER, old_sal NUMBER, new_sal NUMBER,
  changed_by VARCHAR2(30), changed_on DATE);

CREATE OR REPLACE TRIGGER trg_sal_audit
  AFTER UPDATE OF sal ON emp
  FOR EACH ROW
  WHEN (NEW.sal <> OLD.sal)                    -- no colon inside WHEN
BEGIN
  INSERT INTO emp_audit VALUES (:OLD.empno, :OLD.sal, :NEW.sal, USER, SYSDATE);
END;
/
```

```plsql
SQL> UPDATE emp SET sal = sal * 1.10 WHERE deptno = 10;
3 rows updated.
SQL> SELECT empno, old_sal, new_sal FROM emp_audit ORDER BY empno;

     EMPNO    OLD_SAL    NEW_SAL
---------- ---------- ----------
      7782       2450       2695
      7839       5000       5500
      7934       1300       1430
```

Three rows were updated, so the row trigger fired three times and wrote three audit rows (the update itself is uncommitted, and the audit rows roll back with it, which is exactly what an audit must do).

**Example 3: BEFORE UPDATE to enforce a rule.**

```plsql
CREATE OR REPLACE TRIGGER trg_no_pay_cut
  BEFORE UPDATE OF sal ON emp
  FOR EACH ROW
BEGIN
  IF :NEW.sal < :OLD.sal THEN
    RAISE_APPLICATION_ERROR(-20002,
      'Salary cannot be reduced from ' || :OLD.sal || ' to ' || :NEW.sal);
  END IF;
END;
/
```

```plsql
SQL> UPDATE emp SET sal = 700 WHERE empno = 7369;
UPDATE emp SET sal = 700 WHERE empno = 7369
       *
ERROR at line 1:
ORA-20002: Salary cannot be reduced from 800 to 700
ORA-06512: at "SCOTT.TRG_NO_PAY_CUT", line 3
ORA-04088: error during execution of trigger 'SCOTT.TRG_NO_PAY_CUT'
```

**One trigger for several events.** The predicates `INSERTING`, `UPDATING` and `DELETING` let one body serve all three:

```plsql
CREATE OR REPLACE TRIGGER trg_emp_log
  AFTER INSERT OR UPDATE OR DELETE ON emp
  FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO emp_log VALUES ('INSERT', :NEW.empno, SYSDATE);
  ELSIF UPDATING THEN
    INSERT INTO emp_log VALUES ('UPDATE', :NEW.empno, SYSDATE);
  ELSE                                         -- DELETING: :NEW is NULL, use :OLD
    INSERT INTO emp_log VALUES ('DELETE', :OLD.empno, SYSDATE);
  END IF;
END;
/
```

::: caution Common mistake
Do not use `:OLD` in an INSERT trigger or `:NEW` in a DELETE trigger to read a value: they are all NULL there. And do not forget `FOR EACH ROW`: without it the trigger is a statement trigger, and `:NEW` gives a compile error.
:::

**The mutating-table error.** A row trigger may not **read or change the table on which it fires** (except through `:OLD` and `:NEW`), because the table is in the middle of being changed and its state is not consistent. Oracle raises `ORA-04091: table SCOTT.EMP is mutating, trigger/function may not see it`.

```plsql
CREATE OR REPLACE TRIGGER trg_bad
  BEFORE UPDATE OF sal ON emp
  FOR EACH ROW
DECLARE
  v_max NUMBER;
BEGIN
  SELECT MAX(sal) INTO v_max FROM emp;         -- reads EMP while EMP is being updated: ORA-04091
  IF :NEW.sal > v_max THEN NULL; END IF;
END;
/
```

The usual cures are: (1) avoid reading the table (use `:OLD` and `:NEW`, or another table); (2) do the check in a **statement** trigger, which fires when the table is not mutating; (3) use a **compound trigger** (Oracle 11g), which has BEFORE STATEMENT, AFTER EACH ROW and AFTER STATEMENT sections in one body and shares variables between them: collect the keys in the row section, process them in the AFTER STATEMENT section.

## 5.5 INSTEAD OF triggers

A view made from a join, a GROUP BY or DISTINCT is generally **not updatable**. An **INSTEAD OF** trigger is defined on the view and runs **instead of** the DML statement the user issued; its body performs the real changes on the base tables. INSTEAD OF triggers are always row-level, exist only on views, and `:OLD` and `:NEW` refer to the view's columns.

```plsql
CREATE OR REPLACE VIEW v_emp_dept AS
  SELECT e.empno, e.ename, e.sal, d.dname
  FROM   emp e JOIN dept d ON e.deptno = d.deptno;

CREATE OR REPLACE TRIGGER trg_vemp_ii
  INSTEAD OF INSERT OR DELETE ON v_emp_dept
  FOR EACH ROW
BEGIN
  IF INSERTING THEN
    INSERT INTO emp (empno, ename, sal, deptno)
    VALUES (:NEW.empno, :NEW.ename, :NEW.sal,
            (SELECT deptno FROM dept WHERE dname = :NEW.dname));   -- find the department by name
  ELSE
    DELETE FROM emp WHERE empno = :OLD.empno;
  END IF;
END;
/
```

```plsql
SQL> INSERT INTO v_emp_dept VALUES (8100, 'KARKI', 1200, 'SALES');
1 row created.
SQL> SELECT ename, deptno FROM emp WHERE empno = 8100;

ENAME          DEPTNO
---------- ----------
KARKI              30

SQL> DELETE FROM v_emp_dept WHERE empno = 8100;
1 row deleted.
```

Without the trigger the INSERT would fail with `ORA-01779: cannot modify a column which maps to a non-key-preserved table`. With it, users and applications treat the join view as a table, and the trigger decides how the change reaches EMP and DEPT.

## 5.6 Managing triggers, and restrictions

| Task | Statement |
|---|---|
| Turn one trigger off or on | `ALTER TRIGGER trg_sal_audit DISABLE;` / `ENABLE;` |
| Turn all triggers of a table off or on | `ALTER TABLE emp DISABLE ALL TRIGGERS;` |
| Remove a trigger | `DROP TRIGGER trg_sal_audit;` |
| Recompile | `ALTER TRIGGER trg_sal_audit COMPILE;` |
| List triggers | `SELECT trigger_name, trigger_type, triggering_event, status FROM user_triggers WHERE table_name = 'EMP';` |
| See the source and errors | `SELECT text FROM user_source WHERE name = 'TRG_SAL_AUDIT' ORDER BY line;` and `SHOW ERRORS` |
| Control order (11g) | `CREATE TRIGGER t2 ... FOLLOWS t1` |

A trigger is **enabled** by default when created. Disable triggers during a bulk load, and enable them again afterwards.

**Restrictions and good practice**

1. A trigger body may not contain `COMMIT`, `ROLLBACK` or `SAVEPOINT`: it is part of the transaction that fired it. (An autonomous-transaction procedure called from the trigger may commit, for logging.)
2. Keep triggers **short**; call a stored procedure for long logic. The body is limited to 32 KB.
3. Avoid triggers that fire other triggers in a cycle (A updates a table whose trigger updates the table of A).
4. Never put a rule in a trigger that a constraint can enforce.
5. Remember that triggers do not fire for `TRUNCATE`, and not during direct-path loads unless allowed.
6. Name them for what they do and when: `trg_emp_bi` (BEFORE INSERT), `trg_sal_audit`.

**Other kinds, briefly.** **DDL triggers** fire on `CREATE`, `ALTER`, `DROP` (for example to stop a table from being dropped in production). **System-event triggers** fire on `LOGON`, `LOGOFF`, `STARTUP`, `SHUTDOWN` and `SERVERERROR` (for example to record every login). They are created with `ON SCHEMA` or `ON DATABASE` instead of `ON table`.

| | Trigger | Constraint | Stored procedure |
|---|---|---|---|
| Runs | Automatically on an event | Automatically on every change | Only when called |
| Can express | Any PL/SQL rule | A fixed set of rules (NOT NULL, CHECK, UNIQUE, keys) | Any logic |
| Best for | Audit, derived values, cross-table rules | Simple data integrity | Reusable operations |

## 5.7 Summary and exercises

A trigger is a stored PL/SQL block fired by INSERT, UPDATE or DELETE on a table, a DDL or a system event. It is BEFORE, AFTER or INSTEAD OF, at statement or row level; row triggers see `:OLD` and `:NEW`, can be restricted with `WHEN`, and a combined trigger tests `INSERTING`, `UPDATING` and `DELETING`. Order: BEFORE statement, BEFORE row, row, AFTER row, AFTER statement. A row trigger may not read its own table (mutating-table error ORA-04091). INSTEAD OF triggers make complex views updatable. Triggers cannot commit, are managed with ALTER TRIGGER and DROP TRIGGER, and should stay short.

1. Define a database trigger. State five uses.
2. Compare triggers with constraints and with stored procedures.
3. Write the general syntax of CREATE TRIGGER and explain each clause.
4. Distinguish BEFORE and AFTER triggers, and row-level and statement-level triggers.
5. In what order do triggers fire when one UPDATE changes three rows and all four kinds exist?
6. What are `:OLD` and `:NEW`? What do they contain for INSERT, UPDATE and DELETE?
7. Write a trigger that stores the employee name in capitals and the key from a sequence on insert.
8. Write a trigger that logs the old and new salary of every change into an audit table. Explain the WHEN clause.
9. Write a statement trigger that prevents changes to EMP outside the hours 10:00 to 16:00.
10. What is the mutating-table error? Give an example that causes it and two ways to avoid it.
11. What is an INSTEAD OF trigger? Why are they used, and why only on views?
12. How are triggers enabled, disabled and dropped? Why must a trigger not contain COMMIT?
13. A statement updates 5 rows of EMP; EMP has one BEFORE and one AFTER row trigger and one BEFORE and one AFTER statement trigger. How many trigger executions occur in total?

**Answers to the numerical items.** (5) BEFORE statement (1), then for each of the 3 rows BEFORE row, the change, AFTER row, then AFTER statement (1). (13) 1 + 5 + 5 + 1 = 12 executions: statement triggers once each, row triggers once per row each. For the salary audit of Section 5.4 the three rows of department 10 produced three audit rows with the new salaries 2695, 5500 and 1430.

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Differentiate row-level and statement-level triggers.**

A statement-level trigger fires once for the triggering statement, whether it affects zero or many rows, and cannot use `:OLD` or `:NEW`; it suits rules about time or user, for example no changes on Saturday. A row-level trigger is declared `FOR EACH ROW`, fires once per affected row, can use `:OLD` and `:NEW` and a `WHEN` clause; it suits value rules, for example auditing each salary change. If an UPDATE changes 3 rows, the row trigger runs 3 times and the statement trigger once.

**Q2 (5 marks). Explain INSTEAD OF triggers.**

An INSTEAD OF trigger is defined on a view and runs in place of the INSERT, UPDATE or DELETE issued against it. Complex views (joins, GROUP BY, DISTINCT) are not directly updatable; the trigger body performs the corresponding changes on the base tables using `:NEW` and `:OLD`. Example: an INSTEAD OF INSERT trigger on `v_emp_dept` inserts into EMP after looking up the department number by name. INSTEAD OF triggers are always row-level and exist only for views.

**Q3 (10 marks). What is a trigger? Explain its types, syntax and order of firing with examples.**

*Introduction.* A trigger is a stored PL/SQL block that Oracle runs automatically when a specified event occurs.

*Types.* By timing: BEFORE, AFTER, INSTEAD OF. By level: row and statement. By event: INSERT, UPDATE, DELETE, and also DDL and system events.

*Syntax.* `CREATE OR REPLACE TRIGGER name BEFORE|AFTER event ON table [FOR EACH ROW] [WHEN (cond)] BEGIN ... END;`. Row triggers use `:OLD` and `:NEW`; `INSERTING`, `UPDATING` and `DELETING` identify the event.

*Order.* BEFORE statement, then for each row BEFORE row, the change and AFTER row, and finally AFTER statement.

*Example.* `trg_sal_audit` is an AFTER UPDATE OF sal row trigger with `WHEN (NEW.sal <> OLD.sal)` that inserts `:OLD.sal` and `:NEW.sal` into `emp_audit`; raising the pay of department 10 by 10 percent writes three audit rows.

*Conclusion.* Triggers enforce rules and keep audit data automatically, independent of the application.

**Q4 (10 marks). Explain row-level triggers with :OLD and :NEW, and the mutating-table problem.**

*Row triggers.* With `FOR EACH ROW` the trigger runs for each row. `:OLD` holds the row before the change (NULL for INSERT) and `:NEW` the row after (NULL for DELETE). In a BEFORE trigger `:NEW` may be modified.

*Examples.* `trg_emp_bi` fills `:NEW.empno` from a sequence and capitalises `:NEW.ename`; `trg_no_pay_cut` raises `RAISE_APPLICATION_ERROR(-20002, ...)` when `:NEW.sal < :OLD.sal`, so reducing 800 to 700 fails with ORA-20002.

*Mutating table.* A row trigger cannot query or modify its own table, since the table is being changed and is inconsistent; Oracle raises ORA-04091. Example: a BEFORE UPDATE row trigger on EMP running `SELECT MAX(sal) FROM emp`.

*Remedies.* Avoid reading the table, check in a statement-level trigger, or use a compound trigger that collects keys in the row section and processes them in AFTER STATEMENT.

*Conclusion.* Row triggers give precise control of each change, provided the mutating-table rule is respected.
