# Database Programming - BCA 453 (Semester VIII, Elective III, 3 credits)

Study notes for the TU Database Programming elective (course code CACS453 in the TU outline, Year IV / Semester VIII, 6 hours a week: 3 theory and 3 practical). Seven units follow the outline in its order and with its hours (10, 13, 5, 5, 5, 5 and 5). The language is Oracle SQL and PL/SQL; every example uses the classic EMP and DEPT tables so that you can type it into your own lab database.

| Unit | Title | Hours | Outline topics covered |
|---|---|---|---|
| 1 | Introduction of RDBMS | 10 | Oracle architecture, SQL*Plus and its commands (DESCRIBE, LIST, APPEND, CHANGE, INPUT, DEL, CLEAR BUFFER, script files), values at runtime, DDL, DML, DCL, joins, subqueries |
| 2 | PL/SQL | 13 | concepts, architecture, block structure, running a script, DBMS_OUTPUT.PUT_LINE, substitution variables, language fundamentals, DML and transaction control in PL/SQL, IF / CASE, loops (WHILE, FOR, simple, nested, CONTINUE, labels) |
| 3 | PL/SQL Exception | 5 | scope, user-defined exceptions, propagation, RAISE_APPLICATION_ERROR, EXCEPTION_INIT |
| 4 | Database Cursors | 5 | implicit and explicit cursors, cursor loops, cursor FOR loops, parameterised and nested cursors |
| 5 | Database Triggers | 5 | BEFORE and AFTER, row and statement triggers, INSTEAD OF triggers |
| 6 | Record and Procedures | 5 | record types, nested records, anonymous blocks, procedures, IN and OUT parameters |
| 7 | Functions and Package | 5 | creating and invoking functions, optimising execution, packages, extending, instantiation and initialisation |

## Verification

Oracle itself is not available in the build sandbox, so no PL/SQL block was run on Oracle. What was done instead: (1) the SQL of Unit 1 that is shown with real output was executed with SQLite on the same EMP and DEPT data (`fill_script_outputs.py`); (2) every number printed by a PL/SQL example ("Expected output" blocks) was worked out by hand and recomputed by `bca/tools/check_dbprog.py` with an equivalent Python program on the same data. Check the syntax of any block against your own Oracle XE (free) installation, and report differences.

## Source and honesty

Units, topics and hours follow the TU CACS453 outline as reproduced at notebahadur.com and benchpartner.com. The Oracle behaviour described (SQL*Plus commands, exception names and error numbers, cursor attributes, trigger firing order, package initialisation) is standard documented Oracle 11g to 19c behaviour; edge cases that changed in later releases are flagged in the text. No subject-teacher review.
