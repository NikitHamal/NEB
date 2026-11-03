---
subject: Distributed System
grade: BCA Semester 6
unit: 4
title: Coordination: Mutual Exclusion and Leader Election
hours: 7
area: BCA 355 · Distributed System · Unit 4
---

Two nodes of a booking system both read "1 seat left" and both sell it. On one machine a lock prevents this; across machines there is no shared memory and no shared clock to build a lock from. This unit presents the classical message-passing solutions to **distributed mutual exclusion** (who may enter the critical section?) and **leader election** (who is in charge?), and counts the messages they cost.

::: key What this unit gives you
- The requirements of mutual exclusion (safety, liveness, fairness) and the performance measures (messages, delay).
- Centralised, Ricart–Agrawala, Maekawa quorum and token-ring algorithms with verified message counts.
- Election: the Bully and Ring algorithms and their message complexity.
- Why modern systems use leases and consensus-backed coordination services (ZooKeeper, etcd).
:::

## 4.1 The mutual exclusion problem

A set of processes shares a resource and must enter a **critical section** (CS) one at a time. Requirements:

- **Safety:** at most one process in the CS at any time.
- **Liveness:** every request is eventually granted (no deadlock, no starvation).
- **Fairness (ordering):** requests are granted in the order they were made (by happened-before or timestamp).

Algorithms are compared by **messages per CS entry**, **synchronisation delay** (message times between one process leaving the CS and the next entering) and **client delay** (time from request to entry when the system is idle).

## 4.2 Centralised algorithm

One process is the **coordinator**. To enter, a process sends REQUEST; if the CS is free the coordinator replies GRANT, otherwise it queues the request. On exit the process sends RELEASE and the coordinator grants the next in the queue. It costs **3 messages per entry** (request, grant, release), the delay is two message times, and it is fair. Weaknesses: the coordinator is a single point of failure and a bottleneck, and a client that crashes while holding the CS stalls everyone unless the grant is a **lease** that expires.

## 4.3 Ricart–Agrawala (distributed, timestamp-based)

All N processes take part. To enter the CS, process Pᵢ multicasts REQUEST(Tᵢ, i) to the other N − 1 processes, where Tᵢ is its Lamport timestamp. A process Pⱼ receiving a request replies **OK immediately** unless it is itself in the CS, or it is also requesting with a smaller (timestamp, id) pair, in which case it **defers** the reply until it leaves the CS. Pᵢ enters when it has received N − 1 replies, and on leaving sends the deferred replies. Priority is the pair (timestamp, id), which is a total order (ties on timestamp go to the smaller id).

Every entry costs **2(N − 1) messages**: N − 1 requests and N − 1 replies. The simulation below has four processes request at the same time with timestamps 3, 3, 5 and 4; it counts immediate and deferred replies.

```python
N, reqs = 4, {1: 3, 2: 3, 3: 5, 4: 4}
key = lambda p: (reqs[p], p)
deferred = {p: [] for p in reqs}
replies = {p: 0 for p in reqs}
n_req = n_rep = 0
for me in reqs:
    for other in reqs:
        if other == me:
            continue
        n_req += 1
        if key(other) < key(me):
            deferred[other].append(me)
        else:
            replies[me] += 1
            n_rep += 1
order = []
for p in sorted(reqs, key=key):
    assert replies[p] == N - 1
    order.append(p)
    for q in deferred[p]:
        replies[q] += 1
        n_rep += 1
print("entry order:", order)
print(f"messages: {n_req} REQUEST + {n_rep} REPLY = {n_req + n_rep} (2N(N-1) = {2 * N * (N - 1)})")
```
```output
entry order: [1, 2, 4, 3]
messages: 12 REQUEST + 12 REPLY = 24 (2N(N-1) = 24)
```
Processes 1 and 2 have the same timestamp, and process 1 wins on id; process 4 (timestamp 4) beats process 3 (timestamp 5). Each process entered only after collecting all three replies, and the entry order is the order of the priority pairs, which is why the algorithm is fair. Its weaknesses: N points of failure (a crashed process never replies, so a failure detector is required) and message cost that grows linearly with N.

## 4.4 Maekawa's quorum algorithm

Maekawa observed that a process need not ask *everyone*; it is enough to ask a **quorum** if every pair of quorums intersects, because the common member will grant only one request at a time. If each process Pᵢ has a request set Rᵢ with: (1) Rᵢ ∩ Rⱼ ≠ ∅ for all i, j; (2) Pᵢ ∈ Rᵢ; then mutual exclusion holds. Optimal quorums have size about √N, giving about 3√N messages (request, reply, release). A simple construction places the N processes in a √N × √N **grid** and takes each process's quorum to be its **row plus its column**, of size 2√N − 1; any two quorums share at least one cell.

```python
import math
def grid_quorum(i, k):
    r, c = divmod(i, k)
    return {r * k + j for j in range(k)} | {j * k + c for j in range(k)}

for N in (9, 16):
    k = math.isqrt(N)
    Q = [grid_quorum(i, k) for i in range(N)]
    ok = all(Q[a] & Q[b] for a in range(N) for b in range(N))
    K = len(Q[0])
    print(f"N={N}: quorum size {K}, all pairs intersect: {ok}, "
          f"3*(K-1)={3 * (K - 1)} messages vs Ricart-Agrawala {2 * (N - 1)}")
print("quorum of node 4 (N=9):", sorted(grid_quorum(4, 3)))
```
```output
N=9: quorum size 5, all pairs intersect: True, 3*(K-1)=12 messages vs Ricart-Agrawala 16
N=16: quorum size 7, all pairs intersect: True, 3*(K-1)=18 messages vs Ricart-Agrawala 30
quorum of node 4 (N=9): [1, 3, 4, 5, 7]
```
For N = 9 the grid quorum is 5 and the cost 12 messages against 16; for N = 16 it is 18 against 30. The saving widens as N grows. Maekawa's original algorithm can **deadlock** (three processes each locking a different quorum member), so extra messages (INQUIRE, YIELD, FAILED) and timestamps are needed. Quorum systems return in Unit 6 for replicated data.

## 4.5 Token-ring algorithm

Processes are arranged in a logical ring. A single **token** circulates; only the holder may enter the CS, and a process with no interest passes the token on. Safety is obvious (one token); there is no starvation (the token returns within N hops). The cost per entry is between **1 and N − 1 messages** (token hops) when load is low and the token travels idle, and about **1 message** per entry under heavy load. Problems: the token can be lost (a crashed holder), which must be *detected* (a timeout cannot tell a lost token from a long CS) and regenerated safely; and a crashed process breaks the ring unless it can be bypassed.

| Algorithm | Messages per entry | Delay before entry | Weak point |
|---|---|---|---|
| Centralised | 3 | 2 message times | Coordinator crash |
| Ricart–Agrawala | 2(N − 1) | 2 message times (in parallel) | Any crash blocks |
| Maekawa (grid) | 3(2√N − 2) | 2 message times | Deadlock handling |
| Token ring | 1 to N − 1 (low load) | 0 to N − 1 hops | Token loss |

## 4.6 Leader election

Many protocols need one process to act as coordinator, primary or master. If it crashes, the survivors must **elect** a new one: all processes agree on one non-crashed process, typically the one with the **highest id**. Every election algorithm assumes every process knows the ids of all others.

### The Bully algorithm

A process P that notices the coordinator is down starts an election:

1. P sends ELECTION to all processes with a **higher** id.
2. If no one answers, P wins: it sends COORDINATOR to everyone with a lower id.
3. If a higher process answers OK, P stops; the higher process takes over by holding its own election.

The highest-id process always wins, hence "bully". With N = 7 processes and the coordinator 7 crashed, process 3 starts an election. Count ELECTION messages sent (to every higher id, even a dead one), OK replies from live higher processes, and the final COORDINATOR broadcast:

```python
def bully(n, dead, starter):
    alive = [p for p in range(1, n + 1) if p not in dead]
    elect = ok = 0
    active, seen = [starter], set()
    while active:
        p = active.pop(0)
        if p in seen:
            continue
        seen.add(p)
        higher = list(range(p + 1, n + 1))
        elect += len(higher)
        answered = [q for q in higher if q in alive]
        ok += len(answered)
        active.extend(answered)
    coord = len(alive) - 1
    return elect, ok, coord, elect + ok + coord, max(alive)

for starter in (6, 3, 1):
    e, o, c, tot, leader = bully(7, {7}, starter)
    print(f"starter {starter}: ELECTION={e} OK={o} COORDINATOR={c} total={tot} leader={leader}")
```
```output
starter 6: ELECTION=1 OK=0 COORDINATOR=5 total=6 leader=6
starter 3: ELECTION=10 OK=6 COORDINATOR=5 total=21 leader=6
starter 1: ELECTION=21 OK=15 COORDINATOR=5 total=41 leader=6
```
The best case (the highest live process, 6, starts) costs 6 messages: one ELECTION to the dead 7 and five COORDINATOR messages. Process 3 starting costs 21. The worst case, when the lowest process notices, costs 41 messages: every live process starts its own election, so the total is O(N²). The algorithm assumes a **synchronous** system with reliable failure detection; if the old coordinator recovers it simply bullies its way back.

### The Ring algorithm

Processes are in a logical ring. A process that notices the failure sends an ELECTION message with its id to its successor (skipping dead nodes). Each process appends its own id and forwards it. When the message returns to the initiator it has the ids of all live processes; the initiator picks the highest and circulates a COORDINATOR message once around the ring to tell everyone. If two processes start elections at once, both messages circulate and both reach the same result, which is harmless.

```python
def ring(n, dead, starter):
    alive = [p for p in range(1, n + 1) if p not in dead]
    s = alive.index(starter)
    collected = [alive[(s + k) % len(alive)] for k in range(len(alive))]
    return len(alive), len(alive), max(collected)

e, c, leader = ring(7, {7}, 3)
print(f"ring: ELECTION hops={e}, COORDINATOR hops={c}, total={e + c}, leader={leader}")
```
```output
ring: ELECTION hops=6, COORDINATOR hops=6, total=12, leader=6
```
With six live processes the election costs 12 messages regardless of who starts: 2N' where N' is the number of live processes. This is cheaper than the Bully worst case but is always at least 12, whereas the Bully best case is 6. The **Chang–Roberts** refinement forwards an id only if it is greater than the forwarder's own id, reducing the average to O(N log N) messages.

## 4.7 In practice: leases and coordination services

Real systems avoid hand-built election. A **lease** is a lock with an expiry time: the holder must renew it, and if the holder crashes the lease lapses and the lock is free, with no need to detect the crash. Because clocks differ and pauses (garbage collection, a stalled VM) can outlast the lease, a stale holder may still believe it holds the lock, so lock services issue **fencing tokens** (monotonically increasing numbers) which the protected resource checks, rejecting an older token. **ZooKeeper**, **etcd** and **Consul** run a consensus protocol (Zab, Raft; Unit 6) among a few replicas and expose primitives (ephemeral nodes, watches, compare-and-swap) from which leader election and locks are built. Kubernetes controllers elect a leader by renewing a lease object in etcd; Kafka's brokers elect a controller through such a service.

## 4.8 Seeing coordination: shared hardware, quorums and elections

Coordination is needed wherever several machines share one thing: a disk, a database row, a leadership role. Plate 4.1 shows two kinds of shared medium, an old token-passing network card and a modern server room, and Figures 4.1 to 4.3 show three coordination algorithms with the message counts worked out by a program.

```photogrid label="4.1" cols="2" ratio="1.5" caption="Shared media need rules. (a) An ISA Token Ring network card: in a token ring only the station holding the circulating token may transmit, so two stations can never send at once. This is a hardware version of the token-ring mutual-exclusion algorithm of Section 4.5. (b) A server room with cables running between racks: with many machines and cables, deciding which machine owns a resource or acts as leader cannot be left to chance, and the algorithms of this unit decide it by exchanging messages."
@ photo id="bca355/tokenring" cap="Token Ring network card"
fit 1.5
focus 0.5 0.5
call 0.3 0.5 0.4 0.15 "token-ring chip set"
@ photo id="bca401/serverroom" cap="Racks and cabling"
fit 1.5
focus 0.5 0.5
```

```svgfig label="4.1" caption="Ricart-Agrawala with three processes that all want the critical section at once. Their requests carry Lamport timestamps P1 = 5, P2 = 3, P3 = 7. A process replies at once if it is not interested or its own request is later; otherwise it defers the reply. Order of entry by (timestamp, id): P2 (3), P1 (5), P3 (7). Each entry costs 2 x (N - 1) = 4 messages."
f = Fig(580, 250)
for x, nm, ts, col in ((90, "P1", 5, BLUE), (290, "P2", 3, MINT), (490, "P3", 7, SAND)):
    f.box(x - 45, 8, 90, 30, nm + " (ts " + str(ts) + ")", fill=col, stroke=NAVY, size=11, bold=True)
    f.line(x, 38, x, 240, color=SLATE)
f.arrow([(290, 60), (90, 80)], color=RED, label="REQ(3)", lpos=(190, 62))
f.arrow([(290, 66), (490, 86)], color=RED, label="REQ(3)", lpos=(390, 68))
f.arrow([(90, 100), (490, 120)], color=AMBER, label="REQ(5)", lpos=(300, 104))
f.arrow([(90, 106), (290, 130)], color=AMBER)
f.arrow([(490, 140), (290, 160)], color=TEAL)
f.arrow([(490, 146), (90, 170)], color=TEAL, label="REQ(7)", lpos=(330, 150))
f.arrow([(90, 190), (290, 206)], color=TEAL, dash=True)
f.text(290, 226, "P2 enters first (smallest ts); its deferred replies then go to P1, then P3", size=10, color=NAVY, bold=True)
```

```svgfig label="4.2" caption="Maekawa's quorums for nine processes in a 3 x 3 grid. The quorum of a process is its row plus its column, 5 processes. The quorum of process 0 is [0, 1, 2, 3, 6] and of process 8 is [2, 5, 6, 7, 8]. They share [2, 6], so any two quorums intersect and two processes can never both obtain permission from all of their members. A request costs about 3 x (K - 1) = 12 messages with K = 5, against 16 for Ricart-Agrawala."
f = Fig(580, 230)
q0 = [0, 1, 2, 3, 6]
q8 = [2, 5, 6, 7, 8]
for i in range(9):
    r, c = divmod(i, 3)
    x, y = 40 + c * 56, 20 + r * 62
    inA, inB = i in q0, i in q8
    if inA and inB:
        fill, st = SAND, AMBER
    elif inA:
        fill, st = BLUE, NAVY
    elif inB:
        fill, st = MINT, TEAL
    else:
        fill, st = "#f1f5f9", SLATE
    f.box(x, y, 46, 46, str(i), fill=fill, stroke=st, size=14, bold=True)
f.box(240, 20, 330, 46, "blue: quorum of 0 = row 0 + column 0", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(240, 82, 330, 46, "green: quorum of 8 = row 2 + column 2", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(240, 144, 330, 46, "amber: in both, so it can grant only one", fill=SAND, stroke=AMBER, size=11, bold=True)
```

```svgfig label="4.3" caption="The Bully election with six processes where process 6 (the coordinator) has crashed and process 2 notices. Process 2 sends ELECTION to 3, 4, 5 and 6; 3, 4 and 5 answer OK and start their own elections; only 5 gets no answer from 6, so 5 wins and sends COORDINATOR to the others. The program counts 20 messages in total; if the highest living process (5) had noticed first, only 5 messages would be needed."
import math
f = Fig(580, 230)
cx, cy, R = 150, 115, 80
pts = {}
for k in range(6):
    a = -math.pi / 2 + k * 2 * math.pi / 6
    pts[k + 1] = (cx + R * math.cos(a), cy + R * math.sin(a))
for p in (3, 4, 5, 6):
    f.arrow([pts[2], pts[p]], color=AMBER, sw=1.2)
for p in (1, 2, 3, 4, 6):
    pass
for k in range(1, 7):
    x, y = pts[k]
    dead = k == 6
    win = k == 5
    f.circle(x, y, 17, fill=("#e5e7eb" if dead else (MINT if win else BLUE)), stroke=(RED if dead else (TEAL if win else NAVY)), label=str(k), size=13)
f.box(300, 14, 270, 40, "1. 2 sends ELECTION to 3, 4, 5, 6 (4 msgs)", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(300, 62, 270, 40, "2. 3, 4, 5 reply OK (3 msgs), then each", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(300, 110, 270, 40, "   repeats upward: 3+2+2+1+1 more msgs", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(300, 158, 270, 50, "3. 5 hears nothing from 6, wins, sends\nCOORDINATOR to 1, 2, 3, 4 (4 msgs): total 20", fill=MINT, stroke=TEAL, size=10.5, bold=True)
```

### 4.8.1 Eight uses of mutual exclusion and leader election

1. **One writer for a shared record.** If two servers update the same bank balance at the same moment, one update can overwrite the other. A distributed lock lets only one server write at a time. The lock must be released even if its holder crashes, which is why locks are given as leases with a time limit.
2. **Running a job exactly once.** A nightly task such as the end-of-day settlement or the result publication must run on one machine only. If every server ran it, customers could be charged twice. The servers elect a leader, and only the leader starts the task.
3. **Database primary selection.** A replicated database has one primary that accepts writes and several replicas. When the primary fails, the survivors run an election and the winner is promoted. Clients are then told the new address so that writes continue after a short pause.
4. **Cluster managers.** Tools such as Kubernetes keep their cluster state in a small group of nodes that elect a leader using a consensus protocol. The leader orders all changes, and the others follow. If the leader's machine fails, a new one is chosen within seconds.
5. **Shared files and devices.** When several machines use one shared disk or printer, only one may use it at a time. A token or a request queue decides the order. The token ring in Plate 4.1 did this for the network cable itself.
6. **Avoiding the thundering herd.** Instead of letting all clients compete for a resource, a coordinator hands out turns. Ricart-Agrawala and Maekawa do this without a central server, using 16 and 12 messages for nine processes. Fewer messages mean lower delay for every user.
7. **Fairness and ordering.** Lamport timestamps make the order of entry follow the order of requests, so no process waits forever. This matters in a ticketing or admission system where the first applicant should get the seat. Starvation is impossible when the order is fixed by (timestamp, id).
8. **Fault tolerance.** An algorithm must survive crashed processes. The Bully algorithm elects the highest living identifier even if the old leader is gone, and the ring algorithm sends a message around the circle so that every live node learns the winner (12 messages for six nodes). Failure detectors with time-outs trigger these elections.

## Chapter summary

- Mutual exclusion must be safe, live and fair; compare algorithms by messages and delay.
- Centralised: 3 messages; Ricart–Agrawala: 2(N − 1) messages and a timestamp order (24 messages for N = 4 in the simulation); Maekawa: about 3√N messages using intersecting quorums; token ring: token hops, with loss to handle.
- Bully: highest live id wins; best case 6 messages, worst case 41 for N = 7 with the top process dead. Ring: 2 × live processes = 12 messages.
- Leases and fencing tokens plus consensus-backed services replace hand-written algorithms in practice.

## Practice

1. State the three requirements of mutual exclusion.
2. How many messages does the centralised algorithm use per entry? Why is it fragile?
3. In Ricart–Agrawala with N = 10, how many messages does one CS entry cost? When does a process defer a reply?
4. P₁ requests with timestamp 7 and P₂ with timestamp 7. Who enters first in Ricart–Agrawala, and why?
5. Build the Maekawa grid quorum of process 5 for N = 9 (numbered 0 to 8, row by row).
6. Compare Maekawa's and Ricart–Agrawala's message counts for N = 25 using the grid quorum.
7. Describe how a token ring loses and recovers a token.
8. In the Bully algorithm with 5 processes and process 5 dead, process 2 starts an election. List the messages sent.
9. How many messages does the Ring algorithm use for 8 live processes?
10. What is a fencing token and what problem does it solve?

::: note Answers and worked solutions
**1.** Safety (one at a time), liveness (every request eventually granted), fairness (granted in request order).
**2.** Three (request, grant, release). The coordinator is a single point of failure and bottleneck, and a crashed lock holder blocks everyone unless a lease expires.
**3.** 2(10 − 1) = **18**. A process defers when it is in the CS or is itself requesting with a smaller (timestamp, id).
**4.** P₁: the timestamps tie and the smaller id wins, giving a total order.
**5.** Process 5 is in row 1, column 2. Row: {3, 4, 5}; column: {2, 5, 8}. Quorum {2, 3, 4, 5, 8}.
**6.** √25 = 5; quorum 2·5 − 1 = 9; messages 3 × (9 − 1) = 24; Ricart–Agrawala 2 × 24 = 48.
**7.** If the holder crashes, no one has the token. A timeout cannot distinguish a lost token from a long CS, so a regeneration step (election of a regenerator, token ids/epochs) is needed so two tokens never coexist.
**8.** P2 sends ELECTION to 3, 4, 5 (3 messages; 5 is dead). 3 and 4 answer OK (2). P3 sends to 4, 5 (2), 4 answers (1). P4 sends to 5 (1), no answer, so P4 wins and sends COORDINATOR to 1, 2, 3 (3). Total 3 + 2 + 2 + 1 + 1 + 3 = **12**.
**9.** 8 election + 8 coordinator = **16**.
**10.** A number issued with each lock grant that increases every time; the resource rejects requests carrying an older number than one it has already seen, so a paused process whose lease expired cannot corrupt data.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the Ricart-Agrawala algorithm and count its messages.**

*Introduction.* Ricart-Agrawala is a distributed mutual-exclusion algorithm that needs no central coordinator and orders requests by Lamport timestamps (section 4.3, Figure 4.1).

1. **Request.** A process that wants the critical section sends REQUEST(timestamp, id) to all N - 1 others.
2. **Reply rule.** On receiving a request, a process replies immediately if it is not interested, or if its own request is later than the incoming one. If it is in the critical section or has an earlier request, it defers the reply.
3. **Entry.** A process enters when it has received N - 1 replies.
4. **Exit.** On leaving, it sends all deferred replies.
5. **Example.** With timestamps P1 = 5, P2 = 3, P3 = 7 the order of entry is P2, P1, P3.
6. **Cost.** Each entry needs (N - 1) requests and (N - 1) replies = 2(N - 1) messages, which is 4 for N = 3 and 16 for N = 9. A single crashed process blocks everybody unless failures are detected.

*Conclusion.* The algorithm is fair and has no single point of control, but it costs more messages than a central coordinator and is sensitive to crashes.

**Q2 (5 marks). Describe the Bully algorithm with an example.**

*Introduction.* The Bully algorithm elects the live process with the highest identifier as coordinator. It assumes that every process knows the identifiers of all the others (section 4.6, Figure 4.3).

1. **Detection.** A process that finds the coordinator unresponsive sends ELECTION to every process with a higher identifier.
2. **Reply.** Any live higher process answers OK and takes over by starting its own election.
3. **Winning.** A process that receives no OK within a time-out wins and sends COORDINATOR to all lower processes.
4. **Example.** With six processes and process 6 crashed, process 2 starts. The simulation counts 20 messages and process 5 wins. If process 5 starts, only 5 messages are used, so the best case is much cheaper than the worst.
5. **Cost.** The worst case is O(N squared) messages, when the lowest process starts.

*Conclusion.* The algorithm is simple and fast when the highest process starts, but it is message-heavy in the worst case and assumes reliable failure detection.

**Q3 (10 marks). Compare the centralised, Ricart-Agrawala, Maekawa and token-ring mutual-exclusion algorithms. Explain Maekawa's quorums with a diagram.**

*Introduction.* Mutual exclusion lets only one process at a time use a shared resource. A good algorithm gives safety (never two inside), liveness (every request is eventually granted) and fairness (requests granted in order). Algorithms differ in message cost, delay and tolerance of failure (sections 4.2 to 4.5).

*Centralised.* A coordinator grants permission from a queue: request, grant and release make 3 messages per entry. It is simple and fair, but the coordinator is a single point of failure and a bottleneck.

*Ricart-Agrawala.* Every process is asked and all must reply: 2(N - 1) messages, no coordinator, but every process is critical.

*Maekawa.* Each process asks only the members of its quorum. In a grid of nine, the quorum is a row plus a column, 5 processes. The quorums of processes 0 and 8 are [0, 1, 2, 3, 6] and [2, 5, 6, 7, 8]; they intersect in [2, 6], so two processes cannot both be granted permission (Figure 4.2). The cost is about 3(K - 1) = 12 messages for N = 9. Deadlock is possible and needs extra messages to resolve.

*Token ring.* A token circulates; only its holder may enter. The cost is between 1 and N - 1 messages per entry, and messages are passed even when nobody wants the resource. A lost token must be regenerated.

| N | Centralised | Ricart-Agrawala | Maekawa | Token ring |
|---|---|---|---|---|
| 4 | 3 | 6 | 6 | 1 to 3 |
| 9 | 3 | 16 | 12 | 1 to 8 |
| 16 | 3 | 30 | 18 | 1 to 15 |
| 25 | 3 | 48 | 24 | 1 to 24 |
| 100 | 3 | 198 | 54 | 1 to 99 |

| Algorithm | Fault tolerance | Fairness | Delay before entry |
|---|---|---|---|
| Centralised | coordinator single point | yes | 2 messages |
| Ricart-Agrawala | any crash blocks | yes | 2(N - 1) messages in one round |
| Maekawa | crash in quorum blocks | yes, with care | 2 to 3 sqrt(N) messages |
| Token ring | lost token must be rebuilt | ring order | up to N - 1 hops |

*Election.* If the coordinator or token holder fails, a new leader is chosen: the Bully algorithm (20 messages in the six-process example) or the ring algorithm (12 messages for six nodes).

*Conclusion.* The centralised method is best for small systems, quorums reduce messages for large ones, token rings suit steady heavy load, and in practice leases in a coordination service such as ZooKeeper or etcd are used.
