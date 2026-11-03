---
subject: Distributed System
grade: BCA Semester 6
unit: 5
title: Distributed Transactions and Concurrency Control
hours: 7
area: BCA 355 · Distributed System · Unit 5
---

Transferring Rs 5,000 from an account at Bank A to an account at Bank B means two databases must both apply the change or neither may. If Bank A debits and the network then dies, money has vanished. This unit covers how a transaction that spans several servers is made **atomic** (two-phase and three-phase commit), how concurrent transactions are kept **isolated** (locking, timestamps) and how **distributed deadlocks** are found.

::: key What this unit gives you
- ACID properties and the structure of flat, nested and distributed transactions.
- Two-phase commit (2PC): protocol, state traces, message counts and the blocking problem; three-phase commit (3PC).
- Serializability and the conflict graph; two-phase locking, timestamp ordering, optimistic control.
- Distributed deadlock: wait-for graphs, edge chasing, wait-die and wound-wait; sagas for microservices.
:::

## 5.1 Transactions and ACID

A **transaction** is a sequence of operations treated as one unit. Its ACID properties: **Atomicity** (all or nothing), **Consistency** (it moves the database from one valid state to another), **Isolation** (concurrent transactions behave as if run one after another) and **Durability** (committed effects survive crashes). A *distributed* transaction touches data on several servers, so one server's decision to commit must be coordinated with all the others. The client sends `begin`, performs operations that are routed to the servers holding the data, then calls `commit` or `abort`; a **coordinator** (usually the server where the transaction started) runs the commit protocol, and the other servers are **participants**.

## 5.2 Atomic commit: two-phase commit

**Phase 1 (voting).** The coordinator sends PREPARE to all participants. Each participant that can commit forces its updates and a *prepared* record to its log and replies VOTE-COMMIT, after which it can no longer abort unilaterally; a participant that cannot commit replies VOTE-ABORT (and aborts at once). **Phase 2 (decision).** If all voted commit, the coordinator logs COMMIT and sends GLOBAL-COMMIT; if anyone voted abort (or timed out), it logs ABORT and sends GLOBAL-ABORT. Participants apply the decision and acknowledge.

Each participant moves through the states INIT → READY (voted yes) → COMMIT or ABORT. The coordinator's **decision log record** is the commit point: once written, the transaction is committed, even if the coordinator then crashes. The next program runs three scenarios with three participants and counts messages (PREPARE, votes, decisions, acknowledgements):

```python
def run(votes, coord_crash=False):
    n = len(votes)
    states = {p: ["INIT"] for p in votes}
    msgs = n
    for p, v in votes.items():
        states[p].append("READY" if v else "ABORT")
    msgs += n
    if coord_crash:
        return "BLOCKED", states, msgs
    decision = "COMMIT" if all(votes.values()) else "ABORT"
    for p, v in votes.items():
        if v:
            states[p].append(decision)
            msgs += 2
    return decision, states, msgs

cases = [("all yes", {"P1": 1, "P2": 1, "P3": 1}, False),
         ("P2 votes no", {"P1": 1, "P2": 0, "P3": 1}, False),
         ("coordinator crash", {"P1": 1, "P2": 1, "P3": 1}, True)]
for name, votes, crash in cases:
    d, st, m = run(votes, crash)
    trace = " | ".join(f"{p}: {'>'.join(s)}" for p, s in st.items())
    print(f"{name}: {d}, messages={m}, {trace}")
```
```output
all yes: COMMIT, messages=12, P1: INIT>READY>COMMIT | P2: INIT>READY>COMMIT | P3: INIT>READY>COMMIT
P2 votes no: ABORT, messages=10, P1: INIT>READY>ABORT | P2: INIT>ABORT | P3: INIT>READY>ABORT
coordinator crash: BLOCKED, messages=6, P1: INIT>READY | P2: INIT>READY | P3: INIT>READY
```
In the all-yes case the cost is 4N = 12 messages. When P2 votes no, it aborts unilaterally and the decision and acknowledgement go only to the two prepared participants: 10 messages. In the third case the coordinator crashes after collecting votes: P1, P2 and P3 are all stuck in READY. They cannot commit (someone might have voted no) and cannot abort (the coordinator might have decided commit). This is the **blocking problem** of 2PC: prepared participants hold their locks until the coordinator recovers. Participants may ask each other (the *cooperative termination protocol*): if any participant is in INIT or ABORT the group can abort, but if all are READY they must still wait. Production systems reduce the exposure by replicating the coordinator with consensus (Spanner runs 2PC between Paxos groups).

**Recovery.** After a crash a participant reads its log: no prepared record means it may abort; prepared with no decision means it must ask the coordinator; decision present means redo it. A coordinator with no decision record aborts; with a decision record it resends the decision.

## 5.3 Three-phase commit

3PC inserts a **PRE-COMMIT** phase between voting and the decision: CAN-COMMIT / votes, then PRE-COMMIT / acknowledgements, then DO-COMMIT / HAVE-COMMITTED. The invariant is that no participant commits until *all* participants know that everyone voted yes, so in any failure of the coordinator the survivors can decide safely: if any survivor has seen PRE-COMMIT they commit, otherwise they abort. 3PC is **non-blocking** under crash failures with a reliable timeout-based failure detector (a synchronous model) and costs 6N = 18 messages for N = 3 against 12 for 2PC. Under network partitions it can violate atomicity, and because real networks are asynchronous it is rarely deployed; consensus-based commit (Paxos Commit) is the modern alternative.

## 5.4 Concurrency control: serializability

Two operations **conflict** if they belong to different transactions, access the same item and at least one is a write. A schedule is **conflict-serializable** if its **conflict (precedence) graph**, with an edge Tᵢ → Tⱼ whenever an operation of Tᵢ conflicts with and precedes one of Tⱼ, has **no cycle**. In a distributed system serializability must hold *globally*: each server's local schedule can be serializable while the combination is not, if the servers order the same two transactions differently.

- **Two-phase locking (2PL):** a transaction acquires all locks before releasing any (growing then shrinking phase). It guarantees serializability; **strict 2PL** holds write locks until commit, preventing cascading aborts. Each server runs a lock manager for its own data; locks are released after the commit protocol completes.
- **Timestamp ordering:** each transaction gets a global timestamp (Lamport clock plus site id); an operation that would violate timestamp order aborts its transaction. No deadlocks, but more aborts.
- **Optimistic concurrency control:** execute without locks, validate at commit that no conflicting transaction committed meanwhile, abort otherwise. It suits low-conflict workloads.
- **Multiversion (MVCC):** readers see a snapshot, so they never block writers (PostgreSQL, Spanner).

## 5.5 Distributed deadlocks

With locking, transactions can wait for each other in a cycle. A **wait-for graph** (WFG) has an edge Tᵢ → Tⱼ when Tᵢ waits for a lock held by Tⱼ; a cycle means deadlock. In a distributed system each site sees only a *local* WFG. Three transactions can deadlock although every site's local graph is acyclic: T1 waits for T2 at site S1, T2 waits for T3 at S2, and T3 waits for T1 at S3.

```python
def find_cycle(edges):
    graph = {}
    for a, b in edges:
        graph.setdefault(a, []).append(b)
    def dfs(node, path):
        if node in path:
            return path[path.index(node):] + [node]
        for nxt in graph.get(node, []):
            c = dfs(nxt, path + [node])
            if c:
                return c
        return None
    for start in sorted(graph):
        c = dfs(start, [])
        if c:
            return c
    return None

sites = {"S1": [("T1", "T2")], "S2": [("T2", "T3")], "S3": [("T3", "T1")]}
for s, e in sites.items():
    print(s, "local cycle:", find_cycle(e))
union = [edge for e in sites.values() for edge in e]
print("global cycle:", find_cycle(union))

S1 = [(1, "r", "x"), (2, "w", "x"), (1, "w", "x")]
S2 = [(1, "r", "x"), (1, "w", "x"), (2, "r", "x"), (2, "w", "x")]
for name, s in (("S1", S1), ("S2", S2)):
    g = sorted({(a[0], b[0]) for i, a in enumerate(s) for b in s[i + 1:]
                if a[0] != b[0] and a[2] == b[2] and "w" in (a[1], b[1])})
    cyc = find_cycle(g)
    print(name, "edges:", g, "-> serializable" if cyc is None else f"-> NOT serializable, cycle {cyc}")
```
```output
S1 local cycle: None
S2 local cycle: None
S3 local cycle: None
global cycle: ['T1', 'T2', 'T3', 'T1']
S1 edges: T1 to T2 and T2 to T1 -> NOT serializable, cycle [1, 2, 1]
S2 edges: T1 to T2 -> serializable
```
The last two lines test serializability: S1 reads x in T1, lets T2 write it and then lets T1 write: T1 → T2 and T2 → T1, a cycle, so it is not serializable (a lost update). S2 runs T1 entirely before T2 and is serializable.

**Detection.** *Centralised:* sites send their local WFGs to one detector, which can report **phantom deadlocks** because the snapshots were taken at different times. *Distributed edge chasing* (Chandy–Misra–Haas): when a transaction Tᵢ blocks, it sends a **probe** (i, j, k), meaning "started by Tᵢ, sent by Tⱼ, to Tₖ", along the wait edges. A blocked process forwards the probe to the processes it waits for; **if the probe returns to its initiator, there is a deadlock**. No global graph is built. The victim (the youngest or cheapest transaction) is then aborted.

**Prevention** with timestamps (Rosenkrantz): when Tᵢ requests an item held by Tⱼ,

| Scheme | If Tᵢ is **older** than Tⱼ | If Tᵢ is **younger** than Tⱼ |
|---|---|---|
| **Wait-die** | Tᵢ waits | Tᵢ aborts ("dies") and restarts with its original timestamp |
| **Wound-wait** | Tᵢ aborts Tⱼ ("wounds") | Tᵢ waits |

Both guarantee that waiting only goes one way along the age order, so no cycle can form; restarting with the *original* timestamp ensures an aborted transaction eventually becomes the oldest and succeeds. The simplest approach is a **timeout**: abort a transaction that has waited too long; it is crude but works in practice.

## 5.6 Sagas for microservices

A two-phase commit across independently owned microservices is usually impractical (they use different databases and cannot hold locks across the network). A **saga** breaks the business operation into a sequence of local transactions, each with a **compensating action** that semantically undoes it. Order placement: reserve stock, charge the card, schedule delivery. If delivery scheduling fails, run "refund the card" and "release the stock". Sagas give atomicity-by-compensation but not isolation; intermediate states are visible, so designs add flags such as *pending* and idempotent steps with request IDs (Unit 2).

## 5.7 Seeing transactions: logs, graphs and compensations

A transaction is only as trustworthy as the record it leaves on disk, so the first thing to look at is the hardware of durability. Plate 5.1 shows a cash machine, a pioneer of transactions, and a tape used for logs and backups. Figures 5.1 to 5.3 then show the commit protocol, the serializability test and the distributed deadlock, each checked by a short program.

```photogrid label="5.1" cols="3" ratio="1.0" caption="Where transactions matter. (a) A cash machine (ATM): withdrawing money must debit the account and dispense the notes together, or neither; if the power fails between the two steps, a log decides which happened. (b) Jim Gray (1944-2007), who received the 1998 Turing Award for his work on transaction processing, including the ACID properties and the idea of the write-ahead log. (c) A magnetic tape cartridge: tape was long the medium for backups and archived logs, and a log is what allows a crashed participant to find out whether it had voted yes before the failure."
@ photo id="bca304/atm" cap="Cash machine (ATM)"
fit 1.0
focus 0.5 0.45
call 0.5 0.35 0.2 0.12 "screen and keypad"
@ photo id="bca355/gray" cap="Jim Gray"
fit 1.0
focus 0.5 0.75
@ photo id="bca304/tape" cap="Magnetic tape cartridge"
fit 1.0
focus 0.45 0.35
```

```svgfig label="5.1" caption="Two-phase commit with three participants. Phase 1: the coordinator writes PREPARE to its log and asks every participant to vote; each participant that can commit forces a 'prepared' record to disk and votes YES. Phase 2: if all voted YES the coordinator logs COMMIT and tells everyone; otherwise it logs ABORT. The protocol uses 4 x N = 12 messages for N = 3 participants and at least two round trips (70 ms with a 30 ms round trip and 5 ms per forced log write)."
f = Fig(580, 250)
f.box(10, 90, 110, 50, "Coordinator", fill=SAND, stroke=AMBER, size=11, bold=True)
f.box(10, 20, 110, 34, "log: PREPARE", fill=BLUE, stroke=NAVY, size=10, bold=True)
f.box(10, 186, 110, 34, "log: COMMIT", fill=ROSE, stroke=RED, size=10, bold=True)
f.arrow([(65, 54), (65, 90)], color=NAVY)
f.arrow([(65, 140), (65, 186)], color=RED)
for i, y in enumerate((14, 100, 186)):
    f.box(470, y, 100, 50, "Participant " + str(i + 1) + "\nprepared, YES", fill=MINT, stroke=TEAL, size=10, bold=True)
    f.arrow([(120, 108 + i * 8), (470, y + 14)], color=NAVY)
    f.arrow([(470, y + 38), (120, 124 + i * 8)], color=TEAL, dash=True)
f.text(300, 24, "1. PREPARE (vote request)", size=10.5, color=NAVY, bold=True)
f.text(300, 236, "2. votes YES   3. COMMIT to all   4. ACK", size=10.5, color=RED, bold=True)
```

```svgfig label="5.2" caption="The conflict-graph test for serializability, computed by a program. Schedule S1 = r1(A) w1(A) r2(A) w2(A) r1(B) w1(B) r2(B) w2(B) gives the edges T1 to T2: no cycle, so it is conflict-serializable and equivalent to running T1 then T2. Schedule S2 = r1(A) r2(A) w1(A) w2(A) gives the edges T1 to T2 and T2 to T1: T1 and T2 each precede the other, a cycle, so S2 is not serializable (it loses an update)."
f = Fig(580, 170)
f.text(145, 18, "S1: edge T1 to T2 only", size=11, color=TEAL, bold=True)
f.circle(80, 80, 24, fill=MINT, stroke=TEAL, label="T1", size=13)
f.circle(210, 80, 24, fill=MINT, stroke=TEAL, label="T2", size=13)
f.arrow([(104, 80), (186, 80)], color=TEAL, sw=2)
f.text(145, 140, "acyclic: serializable", size=11, color=TEAL, bold=True)
f.text(435, 18, "S2: edges both ways", size=11, color=RED, bold=True)
f.circle(370, 80, 24, fill=ROSE, stroke=RED, label="T1", size=13)
f.circle(500, 80, 24, fill=ROSE, stroke=RED, label="T2", size=13)
f.arrow([(394, 68), (476, 68)], color=RED, sw=2)
f.arrow([(476, 92), (394, 92)], color=RED, sw=2)
f.text(435, 140, "cycle: not serializable", size=11, color=RED, bold=True)
```

```svgfig label="5.3" caption="A distributed deadlock that no site can see alone. Site 1 knows only that T1 waits for T2, site 2 that T2 waits for T3, and site 3 that T3 waits for T1. Each local wait-for graph is acyclic (cycle found at no single site), but the union is the cycle T1, T2, T3, T1 (global cycle: yes). Detection needs the sites to send their edges to a detector (centralised) or to forward probes along the edges (edge chasing)."
f = Fig(580, 200)
for x, nm in ((30, "Site 1"), (220, "Site 2"), (410, "Site 3")):
    f.box(x, 8, 140, 150, "", fill="#f8fafc", stroke=SLATE)
    f.text(x + 70, 26, nm, size=11, color=NAVY, bold=True)
f.circle(70, 100, 20, fill=BLUE, stroke=NAVY, label="T1", size=12)
f.circle(150, 100, 20, fill=BLUE, stroke=NAVY, label="T2", size=12)
f.arrow([(90, 100), (130, 100)], color=RED, sw=2)
f.circle(260, 100, 20, fill=BLUE, stroke=NAVY, label="T2", size=12)
f.circle(340, 100, 20, fill=BLUE, stroke=NAVY, label="T3", size=12)
f.arrow([(280, 100), (320, 100)], color=RED, sw=2)
f.circle(450, 100, 20, fill=BLUE, stroke=NAVY, label="T3", size=12)
f.circle(530, 100, 20, fill=BLUE, stroke=NAVY, label="T1", size=12)
f.arrow([(470, 100), (510, 100)], color=RED, sw=2)
f.text(110, 140, "T1 waits for T2", size=10, color=SLATE)
f.text(300, 140, "T2 waits for T3", size=10, color=SLATE)
f.text(490, 140, "T3 waits for T1", size=10, color=SLATE)
f.text(290, 184, "global graph: T1 to T2 to T3 to T1 = deadlock", size=10.5, color=RED, bold=True)
```

### 5.7.1 Eight practical uses of distributed transactions

1. **Moving money between banks.** A transfer from one bank to another must debit one account and credit the other. A transaction coordinator makes sure that both happen or neither does, so money is never created or lost. Interbank services such as ConnectIPS depend on exactly this guarantee, although the details of their design are not public.
2. **Booking a seat or a ticket.** Reserving a seat, taking the payment and issuing the ticket are separate steps. If payment fails, the seat must be released. A saga does this with compensations: if issuing the ticket fails, it undoes charge wallet and then reserve seat, in reverse order.
3. **Placing an online order.** An order touches the stock service, the payment service and the delivery service, each with its own database. Two-phase commit across all of them would be slow, so many shops use sagas. The customer sees a clear result: order accepted, or order cancelled and refunded.
4. **Seat allocation in admissions.** When a university or an entrance system assigns a seat to a student, it must lower the free-seat count and record the allocation together. Concurrency control keeps two students from taking the last seat. Serializability is the formal word for this protection.
5. **Updating several replicas.** A write that must reach several copies of a record can use atomic commit so that all replicas apply it or none does. This keeps the copies in agreement. The price is 12 messages for three participants and a wait of at least 70 ms in our example.
6. **Inventory and stock control.** Two shops selling from the same warehouse may both try to sell the last item. Locks or timestamps order their updates so that one succeeds and the other is told 'out of stock'. This is the lost-update problem of schedule S2 in Figure 5.2.
7. **Detecting and breaking deadlocks.** When transactions wait for each other across sites, as in Figure 5.3, the system must find the cycle and abort one transaction. Aborting the youngest wastes the least work. Without detection, the transactions would wait for ever.
8. **Recovery after a crash.** The write-ahead log, kept on stable storage as in Plate 5.1(c), records what each participant promised. After a crash a participant reads its log: if it voted YES but has not heard the outcome, it asks the coordinator. This is why every participant forces the 'prepared' record to disk before voting.

## Chapter summary

- Distributed atomic commit uses a coordinator; 2PC votes then decides and costs 4N messages for N participants (12 for N = 3), but blocks when the coordinator crashes in the READY state.
- 3PC adds PRE-COMMIT and avoids blocking only under synchrony; modern systems use consensus-replicated commit instead.
- A schedule is conflict-serializable iff its precedence graph is acyclic; strict 2PL guarantees it; timestamp ordering and optimistic control are alternatives.
- Distributed deadlocks are cycles in the global wait-for graph; edge chasing detects them with probes; wait-die and wound-wait prevent them.
- Sagas replace distributed ACID with local transactions plus compensation.

## Practice

1. State the ACID properties with one sentence each.
2. Describe the two phases of 2PC. What is the commit point?
3. How many messages does a successful 2PC use with 5 participants? How many does 3PC use?
4. Explain why participants in the READY state may block, and what the cooperative termination protocol can and cannot do.
5. Build the conflict graph for r₁(x) w₂(x) w₁(y) r₂(y) and decide serializability.
6. Why is strict 2PL preferred to basic 2PL?
7. T1 waits for T2 at site A; T2 waits for T3 at site B; T3 waits for T1 at site C. Is there a deadlock? Why can't any single site see it?
8. Describe edge chasing and how a deadlock is recognised.
9. Under wait-die, T5 (timestamp 5) requests a lock held by T9, then T9 requests one held by T5. What happens in each case? Repeat for wound-wait.
10. What is a compensating transaction? Give an example for a ticket-booking saga.

::: note Answers and worked solutions
**1.** Atomicity: all or nothing. Consistency: valid state to valid state. Isolation: concurrent transactions appear serial. Durability: committed results survive crashes.
**2.** Phase 1: the coordinator sends PREPARE and collects votes. Phase 2: it logs and broadcasts the decision (commit only if all voted yes) and collects acknowledgements. The commit point is the coordinator's forced write of the COMMIT record.
**3.** 2PC: 4 × 5 = **20**; 3PC: 6 × 5 = **30**.
**4.** A READY participant voted yes and promised to commit if told; it does not know the decision and cannot decide alone. Cooperative termination lets it ask peers: if any peer is in INIT or ABORT it can abort; if all are READY, no one can decide and all wait for the coordinator.
**5.** Conflicts: r₁(x) before w₂(x) gives T1 → T2; w₁(y) before r₂(y) gives T1 → T2. Edges {T1 → T2}, no cycle: serializable (equivalent to T1 then T2).
**6.** It holds write locks until commit, so no transaction reads uncommitted data and no cascading aborts occur.
**7.** Yes: T1 → T2 → T3 → T1 is a cycle. Each site holds one edge only, so each local graph is acyclic.
**8.** A blocked transaction sends a probe (initiator, sender, receiver) to the transactions it waits for; each blocked recipient forwards it. If a probe arrives back at its initiator, a cycle exists and a victim is aborted.
**9.** Wait-die: T5 (older) requests from T9 (younger) so T5 waits; T9 (younger) requests from T5 (older) so T9 aborts and restarts. Wound-wait: T5 (older) wounds T9, which aborts; T9 (younger) requests from T5 and waits.
**10.** An operation that semantically undoes an earlier committed local transaction. Booking saga: reserve seat, charge card, issue ticket; if issuing fails, refund the card and release the seat.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the two-phase commit protocol. What are its message cost and its main weakness?**

*Introduction.* Atomic commit means that all participants of a distributed transaction commit or all abort. Two-phase commit (2PC) achieves this with a coordinator (section 5.2, Figure 5.1).

1. **Phase 1, voting.** The coordinator logs PREPARE and sends it to all participants. Each participant that can commit forces a 'prepared' record to its log and replies YES; one that cannot replies NO and aborts.
2. **Phase 2, decision.** If all vote YES, the coordinator logs COMMIT and sends it to all; if any votes NO or times out, it logs ABORT. Participants obey and send an acknowledgement.
3. **Cost.** With N participants there are 4N messages: N prepares, N votes, N decisions and N acknowledgements. For N = 3 this is 12, and for N = 10 it is 40. With a 30 ms round trip and 5 ms per forced log write the minimum latency is 2 x 30 + 2 x 5 = 70 ms.
4. **Weakness.** If the coordinator crashes after the participants have voted YES, they are in the *uncertain* state and must hold their locks until it recovers: 2PC is a *blocking* protocol.
5. **Fixes.** Three-phase commit adds a pre-commit phase to avoid blocking under a crash (18 messages for N = 3) but fails under partitions; modern systems run the coordinator on a consensus group such as Paxos or Raft.

*Conclusion.* 2PC is simple and gives atomicity, but costs latency and can block, so it is used where participants are few and reliable.

**Q2 (5 marks). What is serializability? Test the schedules S1 and S2 using a conflict graph.**

*Introduction.* A schedule is serializable if its result equals that of some serial execution of the same transactions. It is the correctness criterion of concurrency control (section 5.4, Figure 5.2).

1. **Conflicts.** Two operations of different transactions conflict if they touch the same item and at least one is a write.
2. **Graph.** Draw a node for each transaction and an edge Ti to Tj when an operation of Ti conflicts with a later operation of Tj.
3. **Test.** The schedule is conflict-serializable if and only if the graph has no cycle.
4. **S1.** r1(A) w1(A) r2(A) w2(A) r1(B) w1(B) r2(B) w2(B). The conflicts all go from T1 to T2, edges T1 to T2, so the graph has no cycle and S1 is equivalent to T1 followed by T2.
5. **S2.** r1(A) r2(A) w1(A) w2(A). Edges T1 to T2 and T2 to T1 form a cycle, so S2 is not serializable; both transactions read the old value and one update is lost.

| Schedule | Edges | Cycle | Serializable |
|---|---|---|---|
| S1 | T1 to T2 | no | yes |
| S2 | T1 to T2 and T2 to T1 | yes | no |

*Conclusion.* Two-phase locking and timestamp ordering guarantee acyclic graphs without testing every schedule.

**Q3 (10 marks). Describe the ACID properties and the concurrency-control and deadlock problems of distributed transactions. Include a diagram and a comparison of 2PC, 3PC and sagas.**

*Introduction.* A transaction is a group of operations that the system treats as one unit of work. In a distributed system the data are on several sites, so extra protocols are needed for atomicity, isolation and deadlock handling.

*ACID.* **Atomicity**: all or nothing (atomic commit, Figure 5.1). **Consistency**: the database moves from one valid state to another. **Isolation**: concurrent transactions behave as if serial (serializability, Figure 5.2). **Durability**: committed results survive crashes, which needs a forced log on stable storage.

*Concurrency control.* Two-phase locking (a growing phase and a shrinking phase) guarantees serializability but can deadlock. Timestamp ordering aborts a transaction that arrives too late. Optimistic control runs first and checks for conflict at commit time.

*Distributed deadlock.* Each site sees only part of the wait-for graph; in Figure 5.3 the local graphs are acyclic (no cycle at any single site) but the global graph has a cycle. Detection can be centralised (send all edges to one site), distributed (edge-chasing probes) or avoided with wait-die or wound-wait timestamps. A victim is aborted and restarted.

*Atomic commit and alternatives.* In 2PC the coordinator collects votes and decides: 12 messages for three participants, and participants block if the coordinator fails. 3PC adds a pre-commit step (18 messages) to reduce blocking. Sagas split a long business transaction into local transactions with a compensation for each; if step 3 fails, the compensations run in reverse: undo charge wallet, then undo reserve seat.

| Feature | 2PC | 3PC | Saga |
|---|---|---|---|
| Messages (N = 3) | 12 | 18 | about 2 per step |
| Latency (30 ms RTT) | 70 ms | 105 ms | per step, no waiting for all |
| Isolation | strong, locks held | strong, locks held | weak, intermediate states visible |
| Blocking | yes | less | no |
| Typical use | databases, XA | rare | microservices, bookings |

*Conclusion.* Strong atomicity costs latency and availability. Databases keep ACID with 2PC inside one organisation, while services across organisations use sagas and accept temporary inconsistency, repaired by compensation.
