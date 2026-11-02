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
S1 edges: [(1, 2), (2, 1)] -> NOT serializable, cycle [1, 2, 1]
S2 edges: [(1, 2)] -> serializable
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
