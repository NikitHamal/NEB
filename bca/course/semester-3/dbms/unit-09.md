---
subject: Database Management System
grade: BCA Semester 3
unit: 9
title: Transaction and Concurrency Control
hours: 4
area: BCA 202 · Database Management System · Unit 9
---

A **transaction** is a unit of work that must succeed or fail as a whole: transferring money, booking a seat, placing an order. This unit explains the guarantees a DBMS gives for transactions and how it lets many users work at once without corrupting data.

::: key What this unit gives you
- The transaction concept, ACID, states, atomicity and durability through logging.
- Isolation, serializability (with precedence graphs) and isolation levels.
- Lock-based protocols (2PL), deadlock handling, multiple granularity, timestamp ordering.
:::

## 9.1 Transaction concept and the simple transaction model

A transaction is a sequence of reads and writes on database items that takes the database from one consistent state to another. The simple model uses `read(A)` (disk → memory) and `write(A)` (memory → disk). Transfer of 300 from A to B: read(A); A := A − 300; write(A); read(B); B := B + 300; write(B). If the system fails between the two writes, 300 vanishes.

**ACID properties**

| Property | Meaning | Mechanism |
|---|---|---|
| **Atomicity** | all or nothing | log + undo |
| **Consistency** | transaction preserves integrity constraints | constraints + programmer |
| **Isolation** | concurrent transactions behave as if serial | concurrency control |
| **Durability** | committed changes survive crashes | log + redo, forced to disk at commit |

**States:** *active* → *partially committed* (last statement done) → *committed*; or *active/partially committed* → *failed* → *aborted* (rolled back, then restarted or killed).

```sql
CREATE TABLE account (acc_no INT PRIMARY KEY, balance NUMERIC CHECK (balance >= 0));
INSERT INTO account VALUES (1, 1000), (2, 500);
BEGIN;
UPDATE account SET balance = balance - 300 WHERE acc_no = 1;
UPDATE account SET balance = balance + 300 WHERE acc_no = 2;
SELECT * FROM account ORDER BY acc_no;
ROLLBACK;
SELECT * FROM account ORDER BY acc_no;
BEGIN;
UPDATE account SET balance = balance - 300 WHERE acc_no = 1;
UPDATE account SET balance = balance + 300 WHERE acc_no = 2;
COMMIT;
SELECT * FROM account ORDER BY acc_no;
```
```output
 acc_no | balance 
--------+---------
      1 |     700
      2 |     800
(2 rows)

 acc_no | balance 
--------+---------
      1 |    1000
      2 |     500
(2 rows)

 acc_no | balance 
--------+---------
      1 |     700
      2 |     800
(2 rows)
```

The first listing is the transaction's view before the `ROLLBACK`; the second shows the rollback undid it completely (atomicity); the third shows the `COMMIT` made it permanent (durability).

## 9.2 Atomicity and durability: the log

The DBMS writes a **log** of every update (transaction id, item, old value, new value) before changing the database: **write-ahead logging**. On a crash, **undo** transactions that did not commit (restore old values) and **redo** committed ones whose pages had not reached disk. A **checkpoint** periodically forces dirty pages and writes a marker so recovery starts there instead of at the beginning of the log. **Shadow paging** is an alternative: updates go to new page copies, and commit atomically switches the page-table pointer.

## 9.3 Concurrency problems and isolation

Without isolation, interleaved transactions cause:

| Anomaly | Example |
|---|---|
| **Lost update** | T1 and T2 both read 100, add 10 and 20, write: one update is lost |
| **Dirty read** | T2 reads a value T1 wrote but later rolls back |
| **Non-repeatable read** | T1 reads a row twice and sees different values because T2 updated and committed between |
| **Phantom** | T1 runs a query twice and sees new rows that T2 inserted between |

**SQL isolation levels** trade correctness for speed:

| Level | Dirty read | Non-repeatable read | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | possible | possible | possible |
| READ COMMITTED (default in Oracle, PostgreSQL) | no | possible | possible |
| REPEATABLE READ (MySQL default) | no | no | possible (not in PostgreSQL's snapshot implementation) |
| SERIALIZABLE | no | no | no |

`SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;` chooses the level.

## 9.4 Serializability

A **schedule** is an interleaving of operations of several transactions. A **serial** schedule runs them one after another and is always correct. A schedule is **serializable** if its effect equals some serial schedule. Two operations **conflict** if they belong to different transactions, access the same item and at least one is a write (R–W, W–R, W–W). Schedules are **conflict equivalent** if all conflicting pairs occur in the same order; a schedule is **conflict serializable** if conflict equivalent to a serial one.

**Precedence (serialization) graph:** one node per transaction; an edge Ti → Tj if an operation of Ti conflicts with a *later* operation of Tj. The schedule is conflict serializable **iff the graph has no cycle**; a topological order gives an equivalent serial order.

::: example Worked example: two schedules
**S1:** R1(A) W1(A) R2(A) W2(A) R1(B) W1(B) R2(B) W2(B). The conflicts are W1(A) before R2(A) and W2(A); and W1(B) before R2(B) and W2(B): every edge points T1 → T2. No cycle: **serializable, equivalent to T1 then T2**.
**S2:** R1(A) R2(A) W1(A) W2(A). R2(A) before W1(A) gives T2 → T1; R1(A) before W2(A) gives T1 → T2. A **cycle**: not conflict serializable (it is the lost-update pattern).
:::

**Recoverability.** A schedule is **recoverable** if a transaction commits only after every transaction whose data it read has committed. **Cascading rollback** occurs if a failure forces other transactions that read dirty data to abort too; **cascadeless** schedules read only committed data.

## 9.5 Lock-based protocols

A **lock** controls access to an item: **shared (S)** for reading, **exclusive (X)** for writing.

| Held \ Requested | S | X |
|---|---|---|
| S | granted | wait |
| X | wait | wait |

**Two-phase locking (2PL):** each transaction has a **growing phase** (acquire locks, release none) then a **shrinking phase** (release, acquire none). 2PL guarantees conflict serializability, with the **lock point** (last lock acquired) defining the serial order. **Strict 2PL** holds all X locks until commit/abort, so it avoids cascading rollbacks; **rigorous 2PL** holds all locks until the end. Most DBMSs use strict 2PL. 2PL does **not** prevent deadlock.

## 9.6 Deadlock handling

A **deadlock** is a cycle of transactions each waiting for a lock held by the next. Example: T1 holds X(A) and requests X(B); T2 holds X(B) and requests X(A).

- **Prevention:** order resources and request in that order; or timestamp schemes: **wait–die** (older waits for younger, younger requesting from older dies/aborts) and **wound–wait** (older requesting from younger wounds/aborts it, younger waits for older).
- **Detection:** keep a **wait-for graph** (Ti → Tj if Ti waits for Tj); a cycle = deadlock; choose a **victim** (least work done) and roll it back.
- **Timeout:** abort a transaction waiting too long (simple, may abort needlessly).

## 9.7 Multiple granularity locking

Items can be locked at different **granularities**: database, table, page, row. Fine granularity increases concurrency but costs more locks; coarse is cheap but blocks others. **Intention locks** make this safe: **IS** (intent to take S locks lower down), **IX** (intent to take X locks lower down), **SIX** (S on the whole plus intent for X on parts). A transaction wanting to lock a row first takes the appropriate intention lock on the table (and database).

| Held \ Requested | IS | IX | S | SIX | X |
|---|---|---|---|---|---|
| IS | yes | yes | yes | yes | no |
| IX | yes | yes | no | no | no |
| S | yes | no | yes | no | no |
| SIX | yes | no | no | no | no |
| X | no | no | no | no | no |

## 9.8 Time-stamp based protocol

Each transaction gets a unique **timestamp** TS(T) on starting (older = smaller). Each item Q stores **R-ts(Q)** (largest timestamp of a successful read) and **W-ts(Q)** (largest of a successful write). The protocol enforces serial order by timestamp, with no locks and no deadlocks:

- **T reads Q:** if TS(T) < W-ts(Q) the value T needs was overwritten → **reject, roll back T** (restart with a new timestamp); else allow and set R-ts = max(R-ts, TS(T)).
- **T writes Q:** if TS(T) < R-ts(Q) a younger transaction already read the old value → **reject T**; if TS(T) < W-ts(Q) the write is obsolete → reject (the **Thomas write rule** instead simply *ignores* this write); else allow and set W-ts = TS(T).

::: example Worked example
TS(T1) = 5, TS(T2) = 9. Initially R-ts(A) = W-ts(A) = 0. T2 writes A: allowed, W-ts(A) = 9. T1 then reads A: TS(T1) = 5 < W-ts(A) = 9, so T1 would be reading a value "from the future": **T1 is rolled back** and restarted with a larger timestamp.
:::

## Formula and fact sheet

- ACID: Atomicity, Consistency, Isolation, Durability.
- Conflict = different transactions, same item, at least one write. Serializable iff the precedence graph is acyclic.
- 2PL: growing then shrinking; strict 2PL holds X locks to commit; deadlocks still possible.
- Deadlock: wait-for graph cycle. Wait–die / wound–wait prevent it.
- Intention locks IS, IX, SIX allow multiple granularity.
- Timestamp rules: read rejected if TS < W-ts; write rejected if TS < R-ts (ignored under Thomas rule if only TS < W-ts).

## Chapter summary

- Transactions give ACID; logging provides atomicity and durability.
- Isolation levels and serializability define what concurrent execution may look like; acyclic precedence graphs prove correctness.
- Locking (2PL, strict 2PL), deadlock handling, multiple granularity and timestamps are the standard concurrency-control tools.

## Practice

1. Define transaction; explain each ACID property with a bank-transfer example.
2. Draw the state diagram of a transaction.
3. Explain lost update, dirty read, non-repeatable read and phantom.
4. Test the schedule R1(A) W2(A) W1(A) R2(B) W2(B) R1(B) for conflict serializability.
5. State two-phase locking; why is strict 2PL preferred?
6. T1: lock X(A), lock X(B); T2: lock X(B), lock X(A). What happens? Give two ways to handle it.
7. Under timestamp ordering, TS(T1) = 3, TS(T2) = 8, R-ts(Q) = 8. Can T1 write Q?
8. Differentiate wait–die and wound–wait.
9. Why are intention locks needed?

::: note Answers and worked solutions
**1.** A transaction is a logical unit of work. Transfer: atomic (both debit and credit or neither), consistent (total money unchanged), isolated (other transactions do not see the half-done state), durable (once committed, survives a crash).
**2.** active → partially committed → committed; active → failed; partially committed → failed; failed → aborted.
**3.** See the table in 9.3: lost update (overwrite), dirty read (uncommitted data), non-repeatable read (row changed between two reads), phantom (new rows appear).
**4.** Operations: R1(A), W2(A), W1(A), R2(B), W2(B), R1(B). Conflicts: R1(A)→W2(A): T1 → T2. W2(A)→W1(A): T2 → T1. A cycle: **not conflict serializable**.
**5.** Growing phase, then shrinking phase. Strict 2PL holds exclusive locks until commit, so no transaction reads uncommitted data (no cascading rollback) and the schedule is recoverable.
**6.** A **deadlock**: T1 holds A and waits for B, T2 holds B and waits for A. Handle by detection with a wait-for graph and rolling back a victim, or prevention (lock ordering, wait–die/wound–wait), or timeout.
**7.** TS(T1) = 3 < R-ts(Q) = 8: a younger transaction already read Q, so the write is rejected and **T1 is rolled back**.
**8.** Wait–die: an older requester waits; a younger requester aborts. Wound–wait: an older requester aborts (wounds) the younger holder; a younger requester waits.
**9.** They show a lock at a lower level (row) to the higher level (table) so a request for a whole-table S or X lock can be refused or queued without examining every row.
:::
