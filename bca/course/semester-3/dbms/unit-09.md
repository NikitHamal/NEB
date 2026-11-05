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

## 9.9 Seeing the ideas: transactions, schedules and locks

Transactions are the idea that lets millions of people use one database at the same time without trouble. When you withdraw cash at an ATM or book a seat, a transaction either completes entirely or leaves no trace. The theory was put into its modern form by Jim Gray, who received the Turing Award in 1998 for his work on databases and transaction processing.

```photogrid label="9.1" cols="3" ratio="1.0" caption="Transactions in daily life. (a) Jim Gray, the computer scientist who made transaction processing a science and who is associated with the ACID properties and with locking granularity. (b) A bank ATM: one withdrawal is a transaction that checks the balance, reduces it, records the withdrawal and dispenses the cash, and all of this must happen together or not at all. (c) A railway reservation counter: many counters sell seats at the same time, so the DBMS needs concurrency control to give each seat to only one buyer."
@ photo id="bca202/jimgray" cap="Jim Gray"
fit 1.0
focus 0.5 0.28
@ photo id="bca202/atm" cap="ATM: one withdrawal, one transaction"
fit 1.0
focus 0.5 0.5
@ photo id="bca202/booking" cap="Reservation counter: concurrent sellers"
fit 1.0
focus 0.5 0.5
```

```svgfig label="9.1" caption="Atomicity and durability with a log. Transfer of 300 from account A (1,000) to account B (500). Before each change, the DBMS writes a log record with the old and new value (write-ahead logging). If the system crashes after A has been written but before the transaction commits, recovery reads the log, sees that the transaction never committed and undoes it by restoring A to 1,000, so the database returns to the state before the transfer. If the crash comes after the commit record is on disk, recovery redoes the changes (A = 700, B = 800), which is durability."
f = Fig(580, 230)
steps = [("start", "A=1,000\nB=500", SOFT, SLATE), ("write A", "A=700\nlog: A 1000->700", BLUE, NAVY), ("write B", "B=800\nlog: B 500->800", BLUE, NAVY), ("commit", "log: COMMIT\nflushed to disk", MINT, TEAL)]
for i, (a, b, fl, st) in enumerate(steps):
    x = 8 + i * 144
    f.box(x, 24, 128, 58, "", fill=fl, stroke=st, sw=1.6)
    f.text(x + 64, 38, a, size=11, color=st, bold=True)
    f.text(x + 64, 62, b, size=9, color=SLATE)
    if i < 3:
        f.arrow([(x + 128, 53), (x + 144, 53)], color=SLATE, sw=1.5)
f.box(152, 110, 270, 30, "CRASH here (after write A, before commit)", fill=ROSE, stroke=RED, size=10, bold=True)
f.arrow([(220, 110), (220, 84)], color=RED, sw=1.6)
f.box(8, 160, 270, 56, "Recovery: no COMMIT in the log\nUNDO: put A back to 1,000\nresult: as if nothing happened (atomic)", fill=SAND, stroke=AMBER, size=9.5, bold=True)
f.box(300, 160, 272, 56, "Crash after COMMIT on disk\nREDO: A = 700, B = 800\nresult: committed work survives (durable)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
```

```svgfig label="9.2" caption="The lost-update anomaly. Balance is 100. T1 adds 10 and T2 adds 20. In the bad interleaving both read 100 before either writes: T1 writes 110 and T2 then writes 120, which overwrites T1's result, so 10 is lost and the final balance is 120. Any serial order gives 130. The cure is a lock: if T1 takes an exclusive lock when it reads for update, T2 must wait until T1 commits at 110 and then reads 110 and writes 130. In SQL this is written SELECT ... FOR UPDATE or is handled by a stricter isolation level."
f = Fig(580, 230)
f.text(145, 12, "Without locking (bad)", size=11, color=RED, bold=True)
f.line(75, 20, 75, 200, color=SLATE, sw=1.2); f.line(215, 20, 215, 200, color=SLATE, sw=1.2)
f.text(75, 32, "T1 (+10)", size=10, color=NAVY, bold=True); f.text(215, 32, "T2 (+20)", size=10, color=NAVY, bold=True)
ev = [(55, 75, "read 100"), (80, 215, "read 100"), (105, 75, "write 110"), (130, 215, "write 120"), (155, 75, "commit"), (178, 215, "commit")]
for y, x, s in ev:
    f.box(x - 40, y - 10, 80, 20, s, fill=ROSE if "120" in s else BLUE, stroke=RED if "120" in s else NAVY, size=9, bold=True)
f.text(145, 214, "final = 120: T1's +10 is lost", size=10, color=RED, bold=True)
f.text(435, 12, "With an exclusive lock (good)", size=11, color=TEAL, bold=True)
f.line(365, 20, 365, 200, color=SLATE, sw=1.2); f.line(505, 20, 505, 200, color=SLATE, sw=1.2)
f.text(365, 32, "T1 (+10)", size=10, color=NAVY, bold=True); f.text(505, 32, "T2 (+20)", size=10, color=NAVY, bold=True)
ev2 = [(55, 365, "lock-X, read 100", BLUE, NAVY), (80, 505, "lock-X: WAIT", SAND, AMBER), (105, 365, "write 110, commit", BLUE, NAVY), (130, 505, "granted, read 110", MINT, TEAL), (155, 505, "write 130, commit", MINT, TEAL)]
for y, x, s, fl, st in ev2:
    f.box(x - 55, y - 10, 110, 20, s, fill=fl, stroke=st, size=9, bold=True)
f.text(435, 214, "final = 130: same as a serial schedule", size=10, color=TEAL, bold=True)
```

```svgfig label="9.3" caption="Two graphs that decide correctness. Left: the precedence graph of schedule S1 has a single edge T1 to T2, so it has no cycle and is conflict serializable, equivalent to running T1 and then T2. The graph of S2 (the lost-update pattern R1(A) R2(A) W1(A) W2(A)) has edges both ways, a cycle, so S2 is not serializable. Right: a wait-for graph for the deadlock in which T1 holds a lock on A and waits for B while T2 holds B and waits for A; the cycle means deadlock, and the DBMS breaks it by rolling back one victim transaction."
f = Fig(580, 230)
f.text(70, 12, "S1: no cycle", size=10.5, color=TEAL, bold=True)
f.circle(30, 70, 20, fill=BLUE, stroke=NAVY, label="T1", size=11)
f.circle(110, 70, 20, fill=BLUE, stroke=NAVY, label="T2", size=11)
f.arrow([(50, 70), (90, 70)], color=TEAL, sw=2)
f.text(70, 112, "serializable:\nT1 then T2", size=9.5, color=TEAL, bold=True)
f.text(235, 12, "S2: cycle", size=10.5, color=RED, bold=True)
f.circle(195, 70, 20, fill=ROSE, stroke=RED, label="T1", size=11)
f.circle(275, 70, 20, fill=ROSE, stroke=RED, label="T2", size=11)
f.arrow([(213, 60), (257, 60)], color=RED, sw=2)
f.arrow([(257, 80), (213, 80)], color=RED, sw=2)
f.text(235, 112, "not serializable\n(lost update)", size=9.5, color=RED, bold=True)
f.text(450, 12, "Wait-for graph: deadlock", size=10.5, color=RED, bold=True)
f.circle(395, 70, 20, fill=SAND, stroke=AMBER, label="T1", size=11)
f.circle(505, 70, 20, fill=SAND, stroke=AMBER, label="T2", size=11)
f.arrow([(415, 60), (485, 60)], color=RED, sw=2, label="waits for B", lpos=(450, 50), lsize=8.5)
f.arrow([(485, 82), (415, 82)], color=RED, sw=2, label="waits for A", lpos=(450, 102), lsize=8.5)
f.box(340, 130, 230, 44, "choose a victim, ROLLBACK it,\nthe other continues", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.box(10, 150, 300, 60, "Prevention: wait-die / wound-wait by timestamp\nDetection: wait-for graph, cycle = deadlock\nTimeout: abort anyone who waits too long", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
```

```svgfig label="9.4" caption="Two-phase locking and the timestamp rule. Under two-phase locking a transaction first only acquires locks (growing phase), reaches its lock point when it holds the last lock it will need, and then only releases locks (shrinking phase); it never acquires after it has released, and this guarantees conflict serializability. Right: a timestamp example. T1 has TS = 5 and T2 has TS = 9. After T2 writes A, W-ts(A) = 9, so when the older T1 tries to read A (5 is less than 9) it would see a value from the future and is rolled back and restarted with a new, larger timestamp."
f = Fig(580, 220)
f.text(145, 12, "Two-phase locking", size=10.5, color=NAVY, bold=True)
f.line(20, 190, 280, 190, color=SLATE, sw=1.3)
f.line(20, 190, 20, 30, color=SLATE, sw=1.3)
f.text(10, 28, "locks\nheld", size=8.5, color=SLATE, bold=True, anchor="end")
f.raw('<polyline points="20,190 70,150 120,110 150,70 190,100 230,140 270,190" fill="none" stroke="#0f766e" stroke-width="2.6"/>')
f.line(150, 190, 150, 70, color=RED, sw=1.2, dash=True)
f.text(150, 58, "lock point", size=9.5, color=RED, bold=True)
f.text(85, 168, "growing", size=10, color=TEAL, bold=True)
f.text(225, 168, "shrinking", size=10, color=AMBER, bold=True)
f.text(145, 208, "time", size=9.5, color=SLATE, bold=True)
f.text(435, 12, "Timestamp ordering: TS(T1)=5, TS(T2)=9", size=10, color=NAVY, bold=True)
tl = [(40, "T2 writes A", "allowed, W-ts(A) = 9", MINT, TEAL), (92, "T1 reads A", "5 < W-ts 9: too late", ROSE, RED), (144, "T1 rolled back", "restart, new TS = 12", SAND, AMBER), (190, "T1 reads A", "12 > 9: allowed", MINT, TEAL)]
for y, a, b, fl, st in tl:
    f.box(310, y, 120, 38, a, fill=st, stroke=st, color="#ffffff", size=9.5, bold=True)
    f.box(430, y, 140, 38, b, fill=fl, stroke=st, size=9.5, bold=True)
```

### 9.9.1 Eight benefits of ACID transactions and concurrency control

1. **Money and data are never half done.** Atomicity means a transfer from one account to another either completes or leaves no trace (Figure 9.1). A power cut in the middle of a ConnectIPS or Fonepay payment cannot take money from the sender without giving it to the receiver. Customers can trust the system.
2. **The database always follows its rules.** Consistency means every transaction moves the database from one valid state to another, with keys, constraints and totals still correct. A transaction that would break a rule is rolled back. The data in reports are therefore always meaningful.
3. **Many users work at the same time.** Isolation lets hundreds of counters, web sites and apps use the same tables together. Each transaction behaves as if it ran alone. Without it a busy system would have to serve one customer at a time.
4. **Committed work survives crashes.** Durability, supported by the log, means a result that was reported as saved is still there after a power failure or a restart. A student's examination result entered by the office does not disappear overnight. Recovery by redo restores it.
5. **No lost updates.** Locks make a second writer wait for the first, so two clerks adding to the same balance both have their effect (Figure 9.2). Each update is built on the latest value. Totals in the books remain correct.
6. **No wrong reads.** Isolation levels prevent dirty reads of values that are later rolled back, and stronger levels prevent non-repeatable reads and phantoms. A report that adds up a column sees a consistent snapshot of the data. The level can be chosen to balance accuracy and speed.
7. **Deadlocks are resolved automatically.** The DBMS finds a cycle of waiting transactions (Figure 9.3) and rolls one back, so the system does not freeze. The application only has to retry the failed transaction. Prevention rules such as wait-die reduce the chance of such cycles.
8. **Good performance with safety.** Multiple granularity locking lets the DBMS lock a single row for a small update and a whole table for a big report, using intention locks to keep the two compatible. Fine locks allow high concurrency, and coarse locks are cheap. The designer therefore gets both speed and correctness.

```photogrid label="9.2" cols="2" ratio="1.2" caption="Lock granularity. (a) A bank vault of safe deposit boxes: the bank locks each box separately, so eight customers can open eight different boxes at once. A table lock would be like closing the whole vault whenever one customer opens one box. (b) A discrete-time simulation of 8 tellers and 400 transactions, each touching one of 100 rows and lasting one tick. A table lock needs 400 ticks. Row locks let transactions on different rows run together, and only transactions on the same row wait. If every transaction hits the same row (a hot spot), the gain disappears."
@ photo id="bca202/safebox" cap="Safe deposit boxes: one lock for each box, not one for the vault"
fit 1.2
focus 0.5 0.5
@ svg cap="400 transactions, 8 workers: ticks needed"
import random
def ticks(boxes, workers=8):
    q = list(boxes); t = 0
    while q:
        used, nxt, run = set(), [], 0
        for b in q:
            if run < workers and b not in used:
                used.add(b); run += 1
            else:
                nxt.append(b)
        q = nxt; t += 1
    return t
rnd = random.Random(2081)
spread = [rnd.randrange(100) for _ in range(400)]
hot = [7] * 400
t_table, t_row, t_hot = 400, ticks(spread), ticks(hot)
assert t_hot == 400 and 50 <= t_row < 100
f = Fig(300, 236)
f.text(150, 14, "time to finish 400 transactions", size=10.5, color=NAVY, bold=True)
rows = [("table lock", t_table, RED, ROSE), ("row locks, 100 rows used", t_row, TEAL, MINT), ("row locks, one hot row", t_hot, AMBER, SAND)]
for i, (lab, v, c, bg) in enumerate(rows):
    y = 36 + i * 52
    f.text(8, y, lab, size=10.5, color=c, bold=True, anchor="start")
    w = 220 * v / 400
    f.box(8, y + 6, w, 22, "", fill=bg, stroke=c, r=3, sw=1)
    f.text(w + 16, y + 17, "%d ticks" % v, size=10.5, color=c, bold=True, anchor="start", vmid=True)
f.text(150, 206, "speed-up from row locks: %.1fx" % (t_table / t_row), size=10.5, color=TEAL, bold=True)
f.text(150, 224, "ideal is 8x (8 workers); clashes cost the rest", size=10.5, color=SLATE)
```

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

## Model answers (5 and 10 marks)

**Q1 (5 marks). What is a transaction? Explain the ACID properties with an example.**

*Introduction.* A transaction is a sequence of read and write operations on the database that takes it from one consistent state to another and is treated as one logical unit of work. It ends with `COMMIT` (make permanent) or `ROLLBACK` (undo). The standard example is the transfer of 300 from account A (1,000) to account B (500): read(A), A = A - 300, write(A), read(B), B = B + 300, write(B).

1. **Atomicity.** All operations happen or none does. If the system fails after write(A) and before write(B), the log is used to undo the change, so A returns to 1,000 (Figure 9.1).
2. **Consistency.** The transaction preserves integrity rules. The sum A + B is 1,500 before the transfer and 1,500 after it.
3. **Isolation.** Concurrent transactions do not see each other's partial results. Another transaction must not see A = 700 and B = 500, which would show a total of 1,200.
4. **Durability.** Once the transaction has committed, its changes survive a crash. The log records are forced to disk at commit, and recovery redoes the work if needed.
5. **Mechanisms.** Atomicity and durability come from write-ahead logging with undo and redo, and isolation comes from concurrency control such as locking.

*Conclusion.* ACID together make a transaction a safe unit of work, which is why banks, ticket counters and online shops depend on DBMS transactions.

**Q2 (5 marks). Explain the problems caused by concurrent transactions and the SQL isolation levels.**

*Introduction.* When transactions run at the same time without control, their operations interleave and can give wrong results. Figure 9.2 shows the best-known problem.

1. **Lost update.** T1 and T2 both read 100, add 10 and 20 and write; the second write overwrites the first, so the result is 120 and not 130.
2. **Dirty read.** T2 reads a value written by T1, which later rolls back, so T2 used data that never really existed.
3. **Non-repeatable read.** T1 reads a row twice and gets different values because T2 updated and committed in between.
4. **Phantom.** T1 runs the same query twice and finds new rows inserted by T2.
5. **Isolation levels.** `SET TRANSACTION ISOLATION LEVEL ...` chooses between safety and speed.

| Level | Dirty read | Non-repeatable read | Phantom |
|---|---|---|---|
| READ UNCOMMITTED | possible | possible | possible |
| READ COMMITTED | no | possible | possible |
| REPEATABLE READ | no | no | possible |
| SERIALIZABLE | no | no | no |

*Conclusion.* SERIALIZABLE is the safest and slowest, READ COMMITTED is the usual default, and the designer picks the level that the application can afford.

**Q3 (10 marks). What is serializability? Explain two-phase locking and how a DBMS handles deadlock.**

*Introduction.* A schedule is the order in which the operations of several transactions are executed. A serial schedule, which runs the transactions one after the other, is always correct but slow. A schedule is serializable if its result equals that of some serial schedule, so concurrent execution is allowed as long as it is equivalent to a serial one.

*Conflict serializability.* Two operations conflict if they belong to different transactions, use the same item and at least one is a write. A precedence graph has a node for each transaction and an edge Ti → Tj if an operation of Ti conflicts with a later operation of Tj. A schedule is conflict serializable if and only if the graph has no cycle (Figure 9.3). For S1 = R1(A) W1(A) R2(A) W2(A) R1(B) W1(B) R2(B) W2(B) every edge goes from T1 to T2, so it is equal to the serial order T1, T2. For S2 = R1(A) R2(A) W1(A) W2(A) there are edges both ways, a cycle, so it is not serializable: it is the lost-update pattern.

*Lock-based protocols.* A lock controls access to a data item. A shared (S) lock allows reading by many, an exclusive (X) lock allows writing by one. S is compatible with S only; X is compatible with nothing.

*Two-phase locking (2PL).* Each transaction has a growing phase in which it acquires locks and releases none, then a shrinking phase in which it releases locks and acquires none (Figure 9.4). The moment of the last lock is the lock point. 2PL guarantees conflict serializability. Strict 2PL holds all exclusive locks until commit, which also prevents cascading rollback.

*Deadlock.* A deadlock is a cycle of transactions each waiting for a lock held by the next, as when T1 holds A and wants B while T2 holds B and wants A.
1. **Prevention.** Request locks in a fixed order, or use timestamps: wait-die (an older transaction waits, a younger one that requests a lock held by an older one is aborted) or wound-wait (an older transaction rolls back a younger holder).
2. **Detection.** The DBMS keeps a wait-for graph; a cycle means deadlock, and it chooses a victim, usually the transaction with the least work done, and rolls it back.
3. **Timeout.** A transaction that waits too long is aborted, which is simple but may abort needlessly.

| Method | Idea | Weakness |
|---|---|---|
| Prevention | never allow a cycle | may abort needlessly |
| Detection | find the cycle, kill a victim | graph upkeep |
| Timeout | abort long waiters | wrong guesses |

*Conclusion.* Serializability defines what correct concurrency means, 2PL is the usual way to achieve it, and deadlock handling keeps the lock-based system moving.
