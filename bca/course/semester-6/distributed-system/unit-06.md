---
subject: Distributed System
grade: BCA Semester 6
unit: 6
title: Replication, Consistency Models and Consensus
hours: 8
area: BCA 355 · Distributed System · Unit 6
---

Copies of data make a system faster (read near the user) and more available (survive a server loss), but copies can disagree. Deciding *what a reader is allowed to see* is the subject of consistency models; getting a group of replicas to agree on one value despite crashes is the subject of consensus. This unit connects the two through quorums, the CAP theorem, Paxos and Raft.

::: key What this unit gives you
- Why replicate; primary-backup and state machine replication.
- Consistency models: linearizability, sequential, causal, eventual; client-centric guarantees; CAP and PACELC.
- Quorums with the R + W > N rule, verified by enumeration.
- Paxos and Raft: roles, phases, safety rule and the Raft commit index (with its subtle term rule).
:::

## 6.1 Replication

Reasons to replicate: **availability**, **performance** (local reads, load spread) and **fault tolerance**. The costs: updates must reach all replicas, and concurrent updates must be ordered. Two main designs:

- **Primary-backup (passive):** clients write to the primary, which forwards updates to backups. Simple and gives a single order of writes; on primary failure a backup is promoted (needs election and care that the old primary stops: fencing). Synchronous replication waits for backups (no lost writes, higher latency); asynchronous replication risks losing acknowledged writes at failover.
- **State machine replication (active):** deterministic replicas apply the *same commands in the same order*, so they stay identical. A **consensus** protocol orders the commands (Paxos, Raft); replicas tolerate f crashes with 2f + 1 servers.
- **Multi-leader and leaderless** designs (Dynamo, Cassandra) accept writes at several replicas and reconcile later using vector clocks or last-write-wins; they favour availability over single-order consistency.

## 6.2 Consistency models

A **consistency model** is a contract between the data store and its clients about which values reads may return. From strongest to weakest:

| Model | Guarantee |
|---|---|
| **Linearizability** (atomic/strong) | Every operation appears to take effect instantly at some point between its start and its end; the order respects real time |
| **Sequential consistency** | The result is as if all operations ran in *some* single order that respects each client's own program order (real time ignored) |
| **Causal consistency** | Writes that are causally related are seen by all in the same order; concurrent writes may be seen in different orders |
| **Eventual consistency** | If no new updates arrive, all replicas eventually converge |

**Client-centric guarantees** (for eventually consistent stores): *read-your-writes*, *monotonic reads* (never see older data after newer), *monotonic writes* and *writes-follow-reads*. Sessions pinned to one replica often provide them.

The program below tests these definitions by brute force. An operation is (client, kind, value, start, end) on a register initially 0; a history is accepted if some permutation of the operations is *legal* (each read returns the latest write) and respects the required order: program order for sequential consistency, program order plus "a finished before b started" for linearizability.

```python
from itertools import permutations

def legal(order):
    v = 0
    for _, kind, val, _, _ in order:
        if kind == "W":
            v = val
        elif val != v:
            return False
    return True

def ok(ops, strict):
    for perm in permutations(ops):
        pos = {id(o): i for i, o in enumerate(perm)}
        good = True
        for a in ops:
            for b in ops:
                if a is b:
                    continue
                prog = a[0] == b[0] and a[3] < b[3]
                real = strict and a[4] < b[3]
                if (prog or real) and pos[id(a)] > pos[id(b)]:
                    good = False
        if good and legal(perm):
            return True
    return False

H = {"H1": [("A", "W", 1, 0, 3), ("B", "R", 1, 4, 5)],
     "H2": [("A", "W", 1, 0, 3), ("B", "R", 0, 4, 5)],
     "H3": [("A", "W", 1, 0, 5), ("B", "R", 0, 2, 3), ("B", "R", 1, 4, 6)],
     "H4": [("A", "W", 1, 0, 1), ("B", "R", 1, 2, 3), ("B", "R", 0, 4, 5)]}
for name, h in H.items():
    print(f"{name}: linearizable={ok(h, True)}, sequentially consistent={ok(h, False)}")
```
```output
H1: linearizable=True, sequentially consistent=True
H2: linearizable=False, sequentially consistent=True
H3: linearizable=True, sequentially consistent=True
H4: linearizable=False, sequentially consistent=False
```
H2 is the classic *stale read*: B reads 0 after A's write has finished. It is sequentially consistent (B's read can be ordered before the write) but not linearizable, since real time forbids that order. H3 overlaps the write with two reads, and the order read 0, write 1, read 1 is legal. H4 has B seeing the value go backwards, which no consistent single order explains. Linearizability is **composable** and what most people expect of a lock service or a single-leader database, at the price of latency.

## 6.3 The CAP theorem and PACELC

Brewer's conjecture, proved by Gilbert and Lynch (2002): when a **network partition** (P) splits the system, a replicated data store must choose between **consistency** (C: linearizable, every read sees the latest write, so the minority side must refuse requests) and **availability** (A: every request to a live node gets a response, so replicas may diverge). Partitions happen, so the real choice is CP or AP *during a partition*; with no partition both are possible. **PACELC** adds the daily trade-off: *if Partition then A or C, Else Latency or Consistency.* A system that waits for several replicas gives consistency at the cost of latency. Examples: ZooKeeper, etcd and Spanner are CP; Dynamo and Cassandra default to AP (tunable). "CA" is not an option for a distributed system because it cannot choose not to have partitions.

## 6.4 Quorums

With N replicas, a write waits for W acknowledgements and a read contacts R replicas and takes the newest version. If **R + W > N** every read set shares at least one replica with every write set, so the read sees the latest write. Setting W = N, R = 1 favours reads; W = 1, R = N favours writes; R = W = ⌊N/2⌋ + 1 (majorities) balances them and tolerates ⌊(N − 1)/2⌋ failures. The enumeration below tries every pair of write and read sets:

```python
from itertools import combinations

def check(N, W, R):
    pairs = disjoint = 0
    for w in combinations(range(N), W):
        for r in combinations(range(N), R):
            pairs += 1
            if not set(w) & set(r):
                disjoint += 1
    return pairs, disjoint

for N, W, R in ((5, 3, 3), (5, 2, 3), (3, 2, 2), (3, 1, 3)):
    pairs, dis = check(N, W, R)
    print(f"N={N} W={W} R={R}: R+W>N is {R + W > N}; {pairs} quorum pairs, {dis} disjoint")
```
```output
N=5 W=3 R=3: R+W>N is True; 100 quorum pairs, 0 disjoint
N=5 W=2 R=3: R+W>N is False; 100 quorum pairs, 10 disjoint
N=3 W=2 R=2: R+W>N is True; 9 quorum pairs, 0 disjoint
N=3 W=1 R=3: R+W>N is True; 3 quorum pairs, 0 disjoint
```
For N = 5, W = 2, R = 3 (R + W = N) there are 10 disjoint pairs: a write to replicas {1, 2} followed by a read from {3, 4, 5} returns stale data. Sloppy quorums and hinted handoff (Dynamo) relax even this for availability.

## 6.5 Consensus and Paxos

**Consensus**: processes propose values and must decide one such that (*agreement*) no two decide differently, (*validity*) the decision was proposed and (*termination*) every correct process decides. **Paxos** (Lamport) solves single-value consensus among 2f + 1 acceptors tolerating f crashes and arbitrary message loss, with three roles (proposer, acceptor, learner, often on the same machine):

1. **Prepare.** A proposer picks a unique proposal number n and sends PREPARE(n) to the acceptors. An acceptor that has not promised a number ≥ n promises to ignore lower numbers and replies with the highest-numbered proposal it has already *accepted*, if any.
2. **Accept.** If the proposer gets promises from a **majority**, it sends ACCEPT(n, v), where v is the value of the **highest-numbered accepted proposal among the promises**, or its own value if there was none. An acceptor accepts unless it has promised a higher number.
3. A value is **chosen** when a majority of acceptors have accepted the same proposal; learners are informed.

The rule in step 2 is what makes Paxos safe: any later proposer's majority overlaps the earlier accepting majority, so it *discovers and re-proposes* the possibly chosen value. Here proposer 1 gets only two acceptors to accept X and stalls; proposer 2 wants Y but a promise from acceptor 2 reveals X:

```python
class Acceptor:
    def __init__(self):
        self.promised, self.acc = 0, None
    def prepare(self, n):
        if n > self.promised:
            self.promised = n
            return ("promise", self.acc)
        return None
    def accept(self, n, v):
        if n >= self.promised:
            self.promised, self.acc = n, (n, v)
            return True
        return False

A = {i: Acceptor() for i in range(1, 6)}

def propose(n, value, prep_to, acc_to):
    promises = [p for p in (A[i].prepare(n) for i in prep_to) if p]
    if len(promises) < 3:
        return f"proposal {n}: no majority of promises"
    seen = [p[1] for p in promises if p[1]]
    if seen:
        value = max(seen)[1]
    acks = sum(A[i].accept(n, value) for i in acc_to)
    return f"proposal {n}: proposes {value!r}, accepted by {acks}"

print(propose(1, "X", [1, 2, 3], [1, 2]))
print(propose(2, "Y", [2, 3, 4], [2, 3, 4, 5]))
print("stale proposal 1 retries accept:", sum(A[i].accept(1, "X") for i in (3, 4, 5)), "accepted")
print("acceptor states:", {i: a.acc for i, a in A.items()})
```
```output
proposal 1: proposes 'X', accepted by 2
proposal 2: proposes 'X', accepted by 4
stale proposal 1 retries accept: 0 accepted
acceptor states: {1: (1, 'X'), 2: (2, 'X'), 3: (2, 'X'), 4: (2, 'X'), 5: (2, 'X')}
```
Proposal 2 adopted X, so the value chosen (accepted by a majority) is X, not the Y that proposer 2 wanted; the late accept from proposal 1 is refused. Two competing proposers can keep pre-empting each other (**livelock**), so practical Paxos elects a distinguished proposer. **Multi-Paxos** runs many instances to build a replicated log.

## 6.6 Raft

Raft (Ongaro and Ousterhout, 2014) achieves the same goal with an easier-to-teach structure: **leader election**, **log replication** and **safety**.

- Time is divided into **terms**. A server is a *follower*, *candidate* or *leader*. A follower that hears nothing from a leader for a **randomised election timeout** (for example 150 to 300 ms) becomes a candidate, increments the term, votes for itself and requests votes; a majority makes it leader. Randomised timeouts make split votes rare. A server grants one vote per term and only to a candidate whose log is at least as up to date as its own.
- The leader appends client commands to its log and sends AppendEntries to followers (also as heartbeats). An entry is **committed** once stored on a majority of servers, then applied to each server's state machine.
- **Safety rule:** a leader only commits entries from its **current term** by counting replicas; earlier-term entries become committed indirectly when a later entry is committed.

The commit index is the largest index stored on a majority whose entry has the current term. Here the log has nine entries (terms 1 1 1 1 2 2 2 3 3), the current term is 3, and five servers have match indexes 9, 9, 7, 5, 4 (case A) and 9, 9, 8, 8, 4 (case B):

```python
terms = {1: 1, 2: 1, 3: 1, 4: 1, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3}

def commit_index(match, cur):
    n = len(match)
    for idx in sorted(set(match), reverse=True):
        replicas = sum(1 for m in match if m >= idx)
        if replicas > n // 2 and terms[idx] == cur:
            return idx, replicas
    return None

print("case A:", commit_index([9, 9, 7, 5, 4], 3))
print("case B:", commit_index([9, 9, 8, 8, 4], 3))
```
```output
case A: None
case B: (8, 4)
```
In case A index 7 is on three of five servers, a majority, yet nothing may be committed, because entry 7 comes from term 2. Committing old-term entries by counting replicas is unsafe (Raft paper, Figure 8): a leader could be elected without them and overwrite them. In case B entry 8 (term 3) is on four servers, so commit index = 8, which commits entries 1 to 8 together. Raft clusters have 3 or 5 servers (tolerating 1 or 2 failures); etcd, Consul and CockroachDB use it.

## 6.7 Seeing replication: copies, quorums, proposals and logs

Replication means keeping the same data in more than one place, and consensus means agreeing on what the data are. Plate 6.1 puts a face and a place to the ideas, and Figures 6.1 to 6.3 show a quorum, one round of Paxos and a Raft log, with the numbers computed by programs.

```photogrid label="6.1" cols="3" ratio="1.0" caption="Names behind the ideas. (a) The island of Paxos in Greece, the setting of Leslie Lamport's fable 'The Part-Time Parliament' (1998), in which legislators who wander in and out of the chamber still reach decisions: the story that gave the Paxos algorithm its name. (b) Eric Brewer, who stated in 2000 the conjecture that became the CAP theorem: during a network partition a system must choose between consistency and availability. (c) A corridor of racks in a data hall: every rack holds copies of data that are also held in other halls or cities, so that a fire, a power cut or a flood in one place does not destroy the only copy."
@ photo id="bca355/paxos" cap="Paxos island, Greece"
fit 1.0
focus 0.55 0.5
@ photo id="bca355/brewer" cap="Eric Brewer (CAP theorem)"
fit 1.0
focus 0.5 0.4
@ photo id="bca153/dcrack" cap="Data-hall racks (replicas)"
fit 1.0
focus 0.5 0.5
call 0.35 0.5 0.45 0.12 "replicas"
```

```svgfig label="6.1" caption="Quorums with N = 5 replicas, R = 3 and W = 3. A write is acknowledged by replicas 1, 2 and 3; a later read asks replicas 3, 4 and 5. Because R + W = 6 is greater than N = 5, every read quorum and write quorum share at least one replica (here replica 3), so the read sees the newest version. With each replica 99% available, a quorum of 3 out of 5 is available 99.9990% of the time, better than one machine (99%)."
f = Fig(580, 210)
for i in range(5):
    x = 20 + i * 108
    inw, inr = i < 3, i >= 2
    fill = SAND if (inw and inr) else (BLUE if inw else (MINT if inr else "#f1f5f9"))
    st = AMBER if (inw and inr) else (NAVY if inw else (TEAL if inr else SLATE))
    f.box(x, 50, 90, 60, "Replica " + str(i + 1) + "\n" + ("v2" if inw else "v1"), fill=fill, stroke=st, size=11, bold=True)
f.arrow([(20, 40), (300, 40)], color=NAVY, sw=2)
f.text(160, 28, "write quorum W = 3 (new version v2)", size=10.5, color=NAVY, bold=True)
f.arrow([(560, 126), (236, 126)], color=TEAL, sw=2)
f.text(400, 146, "read quorum R = 3 (asks replicas 3, 4, 5)", size=10.5, color=TEAL, bold=True)
f.text(290, 176, "replica 3 is in both quorums and holds v2, so the read returns the newest value", size=10.5, color=RED, bold=True)
```

```svgfig label="6.2" caption="One round of basic Paxos with one proposer and three acceptors. Phase 1: the proposer sends PREPARE(n = 7); the acceptors promise not to accept lower numbers and return any value they already accepted. Phase 2: the proposer sends ACCEPT(n = 7, value v); a majority (2 of 3) accept and the value is chosen. This costs 4N = 12 messages for N = 3; with a stable leader (multi-Paxos) phase 1 is skipped and only 2N = 6 remain."
f = Fig(580, 230)
f.box(10, 80, 100, 50, "Proposer", fill=SAND, stroke=AMBER, size=11, bold=True)
for i, y in enumerate((10, 80, 150)):
    f.box(470, y, 100, 50, "Acceptor " + str(i + 1), fill=MINT, stroke=TEAL, size=11, bold=True)
    f.arrow([(110, 98), (470, y + 14)], color=NAVY)
    f.arrow([(470, y + 36), (110, 112)], color=TEAL, dash=True)
f.text(290, 20, "1a. PREPARE(7)    1b. PROMISE(7)", size=10.5, color=NAVY, bold=True)
f.text(290, 216, "2a. ACCEPT(7, v)   2b. ACCEPTED: majority = chosen", size=10.5, color=RED, bold=True)
```

```svgfig label="6.3" caption="Raft log replication and the commit index. The leader's log has 7 entries; the followers have matched up to entries 5, 5 and 3 and one is up to date at 7. Sorting the match indices gives [7, 7, 5, 5, 3]; an entry is committed when a majority (3 of 5) store it, so the commit index is the third largest value, 5. Entries 6 and 7 are not yet committed and could still be lost if the leader fails."
f = Fig(580, 230)
names = ["Leader", "Follower A", "Follower B", "Follower C", "Follower D"]
match = [7, 7, 5, 5, 3]
for r, (nm, m) in enumerate(zip(names, match)):
    y = 14 + r * 40
    f.text(60, y + 17, nm, size=10.5, color=NAVY, bold=True, anchor="end")
    for k in range(1, 8):
        x = 70 + (k - 1) * 40
        if k <= m:
            col = MINT if k <= 5 else SAND
            st = TEAL if k <= 5 else AMBER
            f.box(x, y, 36, 30, str(k), fill=col, stroke=st, size=11, bold=True)
        else:
            f.box(x, y, 36, 30, "", fill="#f8fafc", stroke=SLATE)
f.text(360, 120, "green: committed", size=11, color=TEAL, bold=True, anchor="start")
f.text(360, 140, "amber: stored only", size=11, color=AMBER, bold=True, anchor="start")
f.text(360, 160, "blank: follower behind", size=11, color=SLATE, bold=True, anchor="start")
```

### 6.7.1 Eight uses of replication and consensus

1. **Surviving machine failure.** If a record is stored on three machines, the loss of one machine does not lose the record. With each machine 99% available, a majority of two out of three is available 99.9702% of the time. This is why important databases keep at least three copies.
2. **Disaster recovery.** A bank or a national payment switch keeps a second site in another city. If an earthquake or a flood disables the main hall, the backup site takes over with data that are almost current. The distance between the sites forces a choice between faster writes and zero data loss.
3. **Faster reads near the user.** A copy placed close to the reader answers sooner than a distant original. News sites and video platforms place replicas in many countries. Reads from such replicas may be slightly stale, which is the price of speed.
4. **Sharing read load.** Many users reading the same data would overload one server. Read replicas share this load, so the system serves many more readers. A university result page on result day is the typical case.
5. **Configuration and leader election.** Small consensus groups such as etcd and ZooKeeper (running Raft or Zab) store the configuration that a whole cluster agrees on. They also decide which node is leader. Every other service can then trust one answer.
6. **A single agreed order of operations.** A replicated state machine applies the same commands in the same order on every replica, so all replicas stay identical. Consensus is what fixes that order. This is how ledgers and lock services keep copies in step.
7. **Tunable consistency.** Dynamo-style stores let the user choose R and W. With N = 3 and R = W = 1 a read right after a write is stale in 66.7% of cases, with R = W = 2 in 0.0%. The same data store can therefore be set for speed or for safety.
8. **Safe upgrades and maintenance.** A node can be taken out for repair while the others keep serving, because a majority remains. A replacement node catches up from the leader's log. This lets a service be updated with no visible downtime.

## Chapter summary

- Replicate for availability, performance and fault tolerance; state machine replication keeps replicas identical by ordering commands through consensus.
- Models: linearizable ⊃ sequential ⊃ causal ⊃ eventual (in strength). A stale read after a completed write is sequentially consistent but not linearizable (H2).
- CAP: under partition choose consistency or availability; PACELC adds latency vs consistency otherwise.
- Quorums: R + W > N forces intersection; enumeration found 10 disjoint pairs for (N, W, R) = (5, 2, 3) and none for (5, 3, 3).
- Paxos is safe because a new proposer must adopt the highest accepted value from its majority; Raft uses terms, randomised timeouts, majority commit and the current-term rule.

## Practice

1. Distinguish primary-backup and state machine replication.
2. Order linearizability, causal, sequential and eventual consistency from strongest to weakest.
3. History: A writes 1 (finishes at t = 2); B then reads 0 (starts at t = 3). Is it linearizable? Sequentially consistent?
4. State the CAP theorem. Why is "CA" not a real option for a distributed system?
5. N = 7, W = 4. What is the smallest R guaranteeing read-your-latest-write? How many replica failures can writes tolerate?
6. How many disjoint (write, read) pairs exist for N = 4, W = 2, R = 2?
7. In Paxos with 5 acceptors, why does a proposer need promises from 3?
8. Why must a Paxos proposer adopt the highest-numbered accepted value?
9. What are the three roles a Raft server can have, and what starts an election?
10. Match indexes of five servers are 6, 6, 5, 3, 2 and all entries up to 6 are from the current term. What is the commit index?

::: note Answers and worked solutions
**1.** Primary-backup: one server executes and ships state to backups. State machine replication: all replicas execute the same commands in the same order (agreed by consensus).
**2.** Linearizability, sequential, causal, eventual.
**3.** Not linearizable (the read began after the write finished and should see 1). It is sequentially consistent: the read can be ordered before the write.
**4.** When a partition occurs a system cannot provide both linearizable consistency and availability. Partitions cannot be ruled out, so a distributed system chooses CP or AP.
**5.** R + W > 7, so R ≥ 4. Writes need 4 of 7: tolerate 3 failures.
**6.** C(4,2) = 6 write sets; a read set disjoint from a given write set is the complementary 2-set (exactly one), so 6 disjoint pairs out of 36.
**7.** Any two majorities of 5 (3 each) share at least one acceptor, which carries knowledge of any value that may be chosen.
**8.** The acceptor in the overlap may belong to a majority that already accepted a value; re-proposing it ensures a value chosen earlier is never replaced.
**9.** Follower, candidate, leader. A follower whose election timeout expires without hearing from a leader becomes a candidate and starts an election.
**10.** Sorted: index 6 on two servers (not a majority of 5); index 5 on three servers: majority. Commit index = **5**.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain read and write quorums. Show when a read is guaranteed to see the latest write.**

*Introduction.* In a replicated store with N copies, a write is sent to W replicas and a read is answered by R replicas; the numbers R and W control consistency and availability (section 6.4, Figure 6.1).

1. **Write quorum.** A write is successful when W replicas have stored it. The others may still be old.
2. **Read quorum.** A read asks R replicas and returns the value with the newest version number.
3. **Overlap rule.** If R + W > N, every read set shares at least one replica with every write set, so the read sees the latest write. With N = 5, R = 3, W = 3 we have 6 > 5 and the overlap is at least one replica.
4. **Check by program.** Over all choices of replica sets, the fraction of stale reads is 0.0% for (5, 3, 3), but 30.0% for (5, 2, 2) and 66.7% for (3, 1, 1).
5. **Availability.** With each replica 99% available, a quorum of 3 out of 5 is up 99.9990% of the time, and 2 out of 3 is up 99.9702%.

| N | R | W | R + W > N | Stale reads | Write availability | Read availability |
|---|---|---|---|---|---|---|
| 3 | 1 | 1 | no | 66.7% | 99.9999% | 99.9999% |
| 3 | 2 | 2 | yes | 0.0% | 99.9702% | 99.9702% |
| 5 | 1 | 5 | yes | 0.0% | 95.0990% | 100.0000% |
| 5 | 3 | 3 | yes | 0.0% | 99.9990% | 99.9990% |
| 5 | 2 | 2 | no | 30.0% | 100.0000% | 100.0000% |

*Conclusion.* Choosing R + W > N gives strong reads, a small W gives fast writes, and a small R gives fast reads; the three cannot all be maximal.

**Q2 (5 marks). State the CAP theorem. Explain how a system chooses between consistency and availability.**

*Introduction.* The CAP theorem, conjectured by Brewer and proved by Gilbert and Lynch, says that a networked data store cannot have all three of consistency, availability and partition tolerance (section 6.3).

1. **Consistency (C).** Every read sees the latest write, as if there were one copy (linearizability).
2. **Availability (A).** Every request to a working node gets an answer.
3. **Partition tolerance (P).** The system works even if the network splits into groups that cannot talk.
4. **The choice.** Partitions cannot be ruled out in a real network, so the real choice is during a partition: a CP system refuses requests on the minority side to stay consistent; an AP system answers on both sides and reconciles later.
5. **Examples.** A bank ledger and a lock service choose CP. A shopping basket, a social-media feed or a DNS cache choose AP. PACELC adds that even without a partition there is a trade-off between latency and consistency.

*Conclusion.* The system must decide, request by request, what is more important when the network fails: being right or being available.

**Q3 (10 marks). Explain the consensus problem and describe Paxos and Raft. Compare them.**

*Introduction.* Consensus means that a group of processes, some of which may crash, agree on one value. It must satisfy agreement (no two decide differently), validity (the value was proposed) and termination (a decision is eventually made). The FLP result shows that with pure asynchrony termination cannot be guaranteed, so real protocols guarantee safety always and progress when the network is well behaved.

*Paxos.* Roles are proposer, acceptor and learner. In phase 1 a proposer sends PREPARE(n) and the acceptors promise to ignore lower numbers; in phase 2 it sends ACCEPT(n, v) and a majority accepting makes v chosen (Figure 6.2). Basic Paxos needs 4N messages = 20 for five acceptors; multi-Paxos with a stable leader needs 2N = 10. Safety comes from the rule that the proposer must adopt the highest-numbered value already accepted.

*Raft.* Raft splits consensus into leader election, log replication and safety. A follower that hears no heartbeat becomes a candidate and wins with a majority vote in a term. The leader appends commands to its log and sends them to followers; an entry is committed when a majority store it. With match indices [7, 7, 5, 5, 3] the commit index is 5 (Figure 6.3). A new leader must have a log at least as up to date as a majority.

*Fault tolerance.* Both tolerate f crashes with 2f + 1 nodes: five nodes tolerate two, and the majority is three.

| Feature | Paxos | Raft |
|---|---|---|
| Design aim | minimal, proven | understandable |
| Leader | optional (multi-Paxos) | always one per term |
| Log | gaps allowed | no gaps, strictly ordered |
| Nodes for f faults | 2f + 1 | 2f + 1 |
| Used in | Chubby, Spanner | etcd, Consul, CockroachDB |

*Conclusion.* Consensus is the foundation for replicated state machines, lock services and configuration stores. Raft is easier to teach and to implement; Paxos is the older, more general design.
