---
subject: Database Management System
grade: BCA Semester 3
unit: 7
title: Stored Procedures, DML Triggers and Indexing
hours: 5
area: BCA 202 · Database Management System · Unit 7
---

Business logic can live **inside** the database: **stored procedures** are named programs, **triggers** run automatically on data changes, and **indexes** make lookups fast. The syllabus is written around SQL Server/Oracle terms; the examples run on PostgreSQL (PL/pgSQL), and the dialect differences are tabulated.

::: key What this unit gives you
- Creating, altering, dropping and executing stored procedures; parameters, defaults and output.
- Transaction flow inside procedures.
- Triggers: creation, limitations, multi-row behaviour, disabling.
- Indexing: ordered indices, dense/sparse, clustering, B+ trees, hashing, multiple keys, `CREATE`/`DROP INDEX`.
:::

## 7.1 Stored procedures

A **stored procedure** is a named block of SQL and procedural code stored and executed in the server. Benefits: fewer network round trips, reuse, central business rules, security (grant `EXECUTE` without table access), and protection against SQL injection (Unit 8) when parameters are used properly.

| Task | PostgreSQL | Oracle (PL/SQL) | SQL Server (T-SQL) |
|---|---|---|---|
| Create | `CREATE PROCEDURE p(a INT) LANGUAGE plpgsql AS $$ … $$;` | `CREATE OR REPLACE PROCEDURE p(a IN NUMBER) IS BEGIN … END;` | `CREATE PROCEDURE p @a INT AS BEGIN … END` |
| Alter | `CREATE OR REPLACE` / `ALTER PROCEDURE` | `CREATE OR REPLACE` | `ALTER PROCEDURE` |
| Execute | `CALL p(1);` | `EXEC p(1);` | `EXEC p @a = 1;` |
| Drop | `DROP PROCEDURE p;` | `DROP PROCEDURE p;` | `DROP PROCEDURE p;` |
| Output parameter | `OUT` | `OUT` | `@x INT OUTPUT` |
| Return a value | use a **function** (`RETURNS`) | function with `RETURN` | `RETURN n` (status integer) |

```sql
CREATE TABLE account (acc_no INT PRIMARY KEY, holder TEXT, balance NUMERIC(10,2) CHECK (balance >= 0));
INSERT INTO account VALUES (1, 'Sita', 5000), (2, 'Ram', 3000);

CREATE PROCEDURE transfer(src INT, dst INT, amt NUMERIC DEFAULT 100) LANGUAGE plpgsql AS $$
BEGIN
    IF amt <= 0 THEN RAISE EXCEPTION 'amount must be positive'; END IF;
    UPDATE account SET balance = balance - amt WHERE acc_no = src;
    UPDATE account SET balance = balance + amt WHERE acc_no = dst;
END $$;

CALL transfer(1, 2, 500);
CALL transfer(1, 2);
SELECT * FROM account ORDER BY acc_no;
```
```output
 acc_no | holder | balance 
--------+--------+---------
      1 | Sita   | 4400.00
      2 | Ram    | 3600.00
(2 rows)
```

Calling `transfer(1, 2)` used the **parameter default** (100). A procedure body runs inside the caller's transaction: if any statement fails, everything it did is undone.

```sql
CALL transfer(2, 1, 100000);
CALL transfer(1, 2, -5);
SELECT * FROM account ORDER BY acc_no;
```
```output
ERROR:  new row for relation "account" violates check constraint "account_balance_check"
DETAIL:  Failing row contains (2, Ram, -96400.00).
ERROR:  amount must be positive
 acc_no | holder | balance 
--------+--------+---------
      1 | Sita   | 4400.00
      2 | Ram    | 3600.00
(2 rows)
```

The first call tried to overdraw Ram: its first `UPDATE` (the debit) violated the `CHECK`, so the call stopped with an error and nothing changed. The second call was rejected by the procedure's own `RAISE EXCEPTION`. Had the failure come at the *second* `UPDATE`, the debit already applied would have been undone too; a procedure call is all-or-nothing, which is **atomicity**. Balances are unchanged.

**Returning data.** A procedure can use `OUT` parameters; a **function** returns a value and can be used inside `SELECT`.

```sql
CREATE FUNCTION total_balance() RETURNS NUMERIC LANGUAGE sql AS $$ SELECT sum(balance) FROM account $$;
CREATE PROCEDURE get_balance(IN p_acc INT, OUT p_bal NUMERIC) LANGUAGE plpgsql AS $$
BEGIN SELECT balance INTO p_bal FROM account WHERE acc_no = p_acc; END $$;
SELECT total_balance();
CALL get_balance(1, NULL);
DROP FUNCTION total_balance();
DROP PROCEDURE get_balance(INT, NUMERIC);
```
```output
 total_balance 
---------------
       8000.00
(1 row)

  p_bal  
---------
 4400.00
(1 row)
```

## 7.2 Transaction flow in a procedure

In T-SQL and PL/SQL a procedure commonly wraps its work as: `BEGIN TRANSACTION` → statements → on error `ROLLBACK`, otherwise `COMMIT`, using `TRY … CATCH` (SQL Server) or `EXCEPTION WHEN OTHERS THEN ROLLBACK` (Oracle). `SAVEPOINT name` marks a point to which `ROLLBACK TO name` can return without abandoning the whole transaction.

```sql
BEGIN;
UPDATE account SET balance = balance - 1000 WHERE acc_no = 1;
SAVEPOINT after_debit;
UPDATE account SET balance = balance + 1000 WHERE acc_no = 99;
ROLLBACK TO after_debit;
UPDATE account SET balance = balance + 1000 WHERE acc_no = 2;
COMMIT;
SELECT * FROM account ORDER BY acc_no;
```
```output
 acc_no | holder | balance 
--------+--------+---------
      1 | Sita   | 3400.00
      2 | Ram    | 4600.00
(2 rows)
```

The credit to account 99 matched no row, so the script issued `ROLLBACK TO after_debit`, which discards only the work done after the savepoint (here nothing was changed, but the principle holds); the debit before the savepoint is kept, and the credit goes to account 2 instead. `COMMIT` then makes the whole transaction permanent.

## 7.3 DML triggers

A **trigger** is a procedure the DBMS fires automatically on `INSERT`, `UPDATE` or `DELETE` of a table. Uses: audit trails, enforcing complex rules, maintaining derived data, cascading changes. Parts: the **event**, the **timing** (`BEFORE` / `AFTER`, or SQL Server `INSTEAD OF`), the **level** (`FOR EACH ROW` or once per statement), an optional `WHEN` condition, and the **action**. Inside a row trigger `OLD` and `NEW` hold the row before and after the change (SQL Server: the `deleted` and `inserted` pseudo-tables, which can contain **many rows**).

```sql
CREATE TABLE audit_log (id SERIAL PRIMARY KEY, acc_no INT, old_bal NUMERIC, new_bal NUMERIC);

CREATE FUNCTION log_balance() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF NEW.balance <> OLD.balance THEN
        INSERT INTO audit_log (acc_no, old_bal, new_bal) VALUES (OLD.acc_no, OLD.balance, NEW.balance);
    END IF;
    RETURN NEW;
END $$;

CREATE TRIGGER trg_balance AFTER UPDATE ON account FOR EACH ROW EXECUTE FUNCTION log_balance();

UPDATE account SET balance = balance * 1.10;
SELECT acc_no, old_bal, new_bal FROM audit_log ORDER BY id;
```
```output
 acc_no | old_bal | new_bal 
--------+---------+---------
      1 | 3400.00 | 3740.00
      2 | 4600.00 | 5060.00
(2 rows)
```

One statement updated two rows, so the row-level trigger fired **twice**: this is the **multi-row** case. A trigger written as if only one row can change is a classic bug; in SQL Server it must read the whole `inserted` table with set-based SQL, not a single variable.

A **BEFORE** trigger can validate or modify `NEW`, or stop the operation with an error:

```sql
CREATE FUNCTION no_big_withdrawal() RETURNS trigger LANGUAGE plpgsql AS $$
BEGIN
    IF OLD.balance - NEW.balance > 2000 THEN RAISE EXCEPTION 'withdrawal over 2000 not allowed'; END IF;
    RETURN NEW;
END $$;
CREATE TRIGGER trg_limit BEFORE UPDATE ON account FOR EACH ROW EXECUTE FUNCTION no_big_withdrawal();
UPDATE account SET balance = balance - 2500 WHERE acc_no = 1;
UPDATE account SET balance = balance - 500 WHERE acc_no = 1;
SELECT acc_no, balance FROM account ORDER BY acc_no;
```
```output
ERROR:  withdrawal over 2000 not allowed
 acc_no | balance 
--------+---------
      1 | 3240.00
      2 | 5060.00
(2 rows)
```

**Limitations and cautions:** triggers are invisible to application code and hard to debug; they add cost to every write; chains of triggers can recurse; a trigger cannot commit or roll back by itself (it follows the statement's transaction); order of several triggers on one event may be unspecified; bulk loads often disable them.

**Disabling, enabling and dropping:**

```sql
ALTER TABLE account DISABLE TRIGGER trg_balance;
UPDATE account SET balance = balance + 1 WHERE acc_no = 2;
SELECT count(*) AS log_rows_after_disabled_update FROM audit_log;
ALTER TABLE account ENABLE TRIGGER trg_balance;
DROP TRIGGER trg_limit ON account;
```
```output
 log_rows_after_disabled_update 
--------------------------------
                              3
(1 row)
```

The count is 3: two rows from the 10% raise and one from the earlier 500 withdrawal; the update made while the trigger was disabled left no log row. (SQL Server: `DISABLE TRIGGER name ON table`; Oracle: `ALTER TRIGGER name DISABLE`; MySQL has no disable, only drop.)

## 7.4 Indexing: basic concepts

An **index** is an auxiliary structure that maps **search-key** values to record locations, like a book's index. Without one, `WHERE sid = 5000` scans the whole table (O(n)); with a B+ tree index it takes a few block reads (O(log n)). The cost: extra disk space and slower `INSERT`/`UPDATE`/`DELETE` because every index must be maintained.

### Ordered indices

Entries are kept sorted by search key.

| Kind | Description |
|---|---|
| **Primary (clustering) index** | the file itself is sorted on the index key; one per table |
| **Secondary (non-clustering) index** | on a non-ordering field; one entry per record (**dense**) is required, many allowed |
| **Dense index** | an index entry for **every** search-key value |
| **Sparse index** | entries for only **some** keys (typically one per block); only possible on a file sorted by that key; smaller, finds a block then scans it |

::: example Worked example: dense versus sparse
A sorted file of 100,000 records, 20 records per block = 5,000 blocks; an index entry is much smaller, 200 per block. **Dense** index: 100,000 entries = 500 index blocks. **Sparse** (one entry per data block): 5,000 entries = 25 index blocks. A binary search of the sparse index takes ⌈log₂ 25⌉ = 5 reads, plus 1 data block read = **6 block reads**, against about ⌈log₂ 5000⌉ = 13 reads for binary search over the file itself. A multi-level index (an index on the index) pushes this further; the B+ tree is the balanced form of that idea.
:::

### B+ tree and hash indices

- A **B+ tree** index is a balanced multiway tree: internal nodes hold keys and pointers; **all records' pointers are in the linked leaves**, so both equality and **range** queries (`BETWEEN`, `ORDER BY`) are efficient. With a fan-out of about 100, a billion keys fit in height about 5. It is the default index in nearly every DBMS.
- A **hash index** applies a hash function to the key to find a bucket: O(1) for **equality** only; no range queries or ordering.
- A **bitmap index** (Oracle, warehouses) stores one bit-vector per distinct value; good for low-cardinality columns such as gender.

### Multiple-key access

An index on **composite** keys `(dept_id, city)` is sorted by dept_id, then city. It speeds `WHERE dept_id = 10 AND city = 'X'` and `WHERE dept_id = 10` (a *prefix*), but **not** `WHERE city = 'X'` alone. Put the most frequently tested, most selective column first. Alternatives for multi-attribute queries are separate indices combined by intersecting their record-id lists, grid files and R-trees (spatial data).

### Creating and dropping indexes

```sql
CREATE TABLE student (sid INT PRIMARY KEY, name TEXT, dept_id INT, city TEXT);
INSERT INTO student SELECT g, 'student' || g, g % 4, 'city' || (g % 7) FROM generate_series(1, 1000) g;
CREATE INDEX idx_student_name ON student (name);
CREATE UNIQUE INDEX idx_student_dc ON student (sid, dept_id);
CREATE INDEX idx_dept_city ON student (dept_id, city);
SELECT indexname FROM pg_indexes WHERE schemaname = current_schema() AND tablename = 'student' ORDER BY indexname;
DROP INDEX idx_student_name;
DROP INDEX idx_student_dc;
SELECT indexname FROM pg_indexes WHERE schemaname = current_schema() AND tablename = 'student' ORDER BY indexname;
```
```output
    indexname     
------------------
 idx_dept_city
 idx_student_dc
 idx_student_name
 student_pkey
(4 rows)

   indexname   
---------------
 idx_dept_city
 student_pkey
(2 rows)
```

The primary key automatically created `student_pkey`, and `UNIQUE` constraints create unique indexes. Syntax is the same in Oracle and MySQL (`DROP INDEX name ON table` in MySQL and SQL Server). **Rules of thumb:** index primary and foreign keys and columns used in `WHERE`, `JOIN` and `ORDER BY`; do not index small tables, columns with few distinct values (except bitmap), or columns updated constantly; check with `EXPLAIN` that the index is used (Unit 8).

## Formula and fact sheet

- Procedures: create, alter, execute (`CALL`/`EXEC`), drop; parameters IN/OUT/default; function returns a value.
- Trigger = event + timing + level + action; `OLD`/`NEW`; **must handle multi-row** statements.
- Dense index: entry per record; sparse: entry per block (sorted file only).
- B+ tree: ordered, range-friendly, height ≈ log_fanout n; hash: equality only.
- Composite index (a, b) serves a and (a, b), not b alone.
- Index cost: space + slower writes.

## Chapter summary

- Stored procedures package logic server-side with parameters, defaults, outputs and transaction control; savepoints allow partial rollback.
- Triggers react to data changes for audit and validation, with caveats about multi-row events, hidden logic and cost.
- Indexes (primary, secondary, dense, sparse, B+ tree, hash, composite) trade space and write speed for read speed.

## Practice

1. List the steps and syntax to create, execute, alter and drop a stored procedure in your lab DBMS.
2. Write a procedure `raise_marks(cid, n)` that adds n marks to every enrolment of a course (cap at 100).
3. Differentiate a procedure and a function.
4. Write a trigger to record deleted students in `student_archive`.
5. Why must a trigger be written for multi-row statements?
6. How do you disable and re-enable a trigger?
7. Differentiate dense and sparse, primary and secondary indexes.
8. A file has 1,000,000 records, 50 per block; index entries fit 500 per block. Compute the dense and sparse index sizes in blocks.
9. Which queries can use an index on (dept_id, city)?

::: note Answers and worked solutions
**1.** PostgreSQL: `CREATE PROCEDURE … LANGUAGE plpgsql AS $$ … $$; CALL p(…); CREATE OR REPLACE PROCEDURE …; DROP PROCEDURE p;` (Oracle `EXEC`, SQL Server `EXEC`/`ALTER PROCEDURE`).
**2.** `CREATE PROCEDURE raise_marks(p_cid CHAR, n INT) LANGUAGE sql AS $$ UPDATE enrollment SET marks = LEAST(marks + n, 100) WHERE cid = p_cid $$;`
**3.** A procedure performs actions, is invoked with `CALL`/`EXEC`, may have OUT parameters; a function returns a value and can appear inside a query.
**4.** `CREATE FUNCTION arch() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN INSERT INTO student_archive SELECT OLD.*; RETURN OLD; END $$; CREATE TRIGGER t AFTER DELETE ON student FOR EACH ROW EXECUTE FUNCTION arch();`
**5.** One statement can change many rows; code that assumes one row (reads a single variable) silently handles only one of them. Row-level triggers fire per row; SQL Server triggers must process the whole `inserted`/`deleted` sets.
**6.** `ALTER TABLE t DISABLE TRIGGER name;` / `ENABLE TRIGGER name;` (Oracle `ALTER TRIGGER name DISABLE|ENABLE`).
**7.** Dense: every key has an entry; sparse: one per block. Primary: on the file's sort key (one per table); secondary: on another field, always dense, many allowed.
**8.** Data blocks = 1,000,000 / 50 = 20,000. Dense: 1,000,000 entries / 500 = **2,000** index blocks. Sparse: 20,000 entries / 500 = **40** blocks.
**9.** Queries filtering on dept_id, or on dept_id and city; not on city alone.
:::
