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
