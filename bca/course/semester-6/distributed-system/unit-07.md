---
subject: Distributed System
grade: BCA Semester 6
unit: 7
title: Fault Tolerance and Distributed File Systems
hours: 5
area: BCA 355 · Distributed System · Unit 7
---

In a cluster of a thousand machines something is always broken. Fault tolerance is therefore not an extra but the main design constraint, and distributed file systems are where the ideas of this book meet real products: replication, consistency, naming and recovery in one service.

::: key What this unit gives you
- Failure terminology, failure detection and the redundancy needed per failure model.
- The Byzantine Generals Problem and the n ≥ 3f + 1 bound, with a verified OM(1) simulation.
- Checkpointing, recovery and the Chandy–Lamport snapshot (with a conserved-total check).
- Distributed file systems: NFS, AFS, GFS and HDFS, with block and replica arithmetic.
:::

## 7.1 Dependability and failure detection

A **fault** causes an **error** that may lead to a **failure** of the service. Faults are *transient* (a dropped packet), *intermittent* or *permanent*. **Dependability** covers availability, reliability, safety and maintainability. The main technique is **redundancy**: information (checksums, erasure codes), time (retry) and physical (replicas).

**Failure detection.** In an asynchronous network a crashed node and a slow one look the same. Detectors use **heartbeats** or pings with a timeout: a node silent for longer than the timeout is *suspected*. Detectors are **complete** (every crashed node is eventually suspected) but not always **accurate** (a live node may be wrongly suspected), and the timeout trades detection speed against false alarms. The *phi-accrual* detector (Cassandra) outputs a suspicion level from the heartbeat history instead of a binary answer.

**Resilience by group size.** To tolerate **f crash (fail-stop)** failures a replicated service needs f + 1 replicas if any survivor's answer can be trusted, and **2f + 1** if a majority must agree (consensus, Unit 6). To tolerate **f Byzantine** failures it needs **3f + 1**.

## 7.2 Byzantine agreement

Lamport, Shostak and Pease (1982) pose the **Byzantine Generals Problem**: a commander and n − 1 lieutenants must agree on attack or retreat though up to f of them are traitors who may lie, so that (IC1) all loyal lieutenants obey the same order and (IC2) if the commander is loyal, they obey his order. **Without signatures, agreement is possible if and only if n ≥ 3f + 1.** Intuition: with n = 3 and one traitor, a lieutenant that hears "attack" from the commander and "he said retreat" from the other lieutenant cannot tell whether the commander or the other lieutenant is lying, since both cases look identical to it.

The oral-messages algorithm **OM(1)**: the commander sends its value to every lieutenant; each lieutenant relays the value it received to every other lieutenant; each lieutenant takes the **majority** of the values it holds (its own and the relays), defaulting to *retreat* (0) on a tie. The simulation lets a traitor commander send alternating values or a traitor lieutenant flip every relay:

```python
def om1(n, traitor):
    lts = range(1, n)
    got = {l: (l % 2 if traitor == 0 else 1) for l in lts}
    decide = {}
    for l in lts:
        votes = [got[l]]
        for o in lts:
            if o != l:
                votes.append(1 - got[o] if o == traitor else got[o])
        ones = sum(votes)
        decide[l] = 1 if 2 * ones > len(votes) else 0
    return decide

for n, traitor in ((4, 0), (4, 2), (3, 0), (3, 2)):
    d = om1(n, traitor)
    loyal = {l: v for l, v in d.items() if l != traitor}
    agree = len(set(loyal.values())) <= 1
    valid = "n/a" if traitor == 0 else all(v == 1 for v in loyal.values())
    who = "commander" if traitor == 0 else f"lieutenant {traitor}"
    print(f"n={n}, traitor={who}: loyal decisions {loyal}, agreement={agree}, validity={valid}")
for f in range(1, 6):
    print(f"f={f}: Byzantine needs n>={3 * f + 1}, crash needs n>={2 * f + 1}")
```
```output
n=4, traitor=commander: loyal decisions {1: 1, 2: 1, 3: 1}, agreement=True, validity=n/a
n=4, traitor=lieutenant 2: loyal decisions {1: 1, 3: 1}, agreement=True, validity=True
n=3, traitor=commander: loyal decisions {1: 0, 2: 0}, agreement=True, validity=n/a
n=3, traitor=lieutenant 2: loyal decisions {1: 0}, agreement=True, validity=False
f=1: Byzantine needs n>=4, crash needs n>=3
f=2: Byzantine needs n>=7, crash needs n>=5
f=3: Byzantine needs n>=10, crash needs n>=7
f=4: Byzantine needs n>=13, crash needs n>=9
f=5: Byzantine needs n>=16, crash needs n>=11
```
With n = 4 both traitor positions are handled. With n = 3 and a traitor lieutenant, the loyal lieutenant sees one 1 and one 0, defaults to 0 and **disobeys a loyal commander**, so IC2 fails. Extending to f traitors needs OM(f) with f + 1 rounds of messages and n ≥ 3f + 1. With **digital signatures** a traitor cannot forge relays and n ≥ f + 2 suffices for agreement. Practical Byzantine-fault-tolerant systems (PBFT, Tendermint, blockchain consensus) use 3f + 1 replicas and quorums of 2f + 1, so two quorums overlap in at least f + 1 replicas, at least one of them honest.

## 7.3 Recovery: checkpoints and snapshots

**Backward recovery** rolls the system back to a saved consistent state and re-executes: processes write **checkpoints** to stable storage. **Independent** checkpointing risks the **domino effect** (rolling back one process forces another back, and so on, possibly to the start); **coordinated** checkpointing saves a consistent global state at once; **message logging** replays deterministic messages from the last checkpoint. **Forward recovery** moves to a new correct state using redundancy (error-correcting codes).

The **Chandy–Lamport snapshot** records a consistent global state without stopping the system, assuming FIFO channels. The initiator records its own state and sends a **MARKER** on every outgoing channel. A process receiving its *first* marker records its state, records that channel as empty, sends markers on all outgoing channels and starts recording messages arriving on its *other* incoming channels. A later marker on a channel stops recording it, and the recorded messages are that channel's state. Two processes P and Q start with balances 100 and 50 (total 150) and exchange transfers; the snapshot must still total 150:

```python
from collections import deque
bal = {"P": 100, "Q": 50}
ch = {("P", "Q"): deque(), ("Q", "P"): deque()}
snap, state, recording = {}, {}, set()

def start(p, from_ch=None):
    snap[p] = bal[p]
    for c in ch:
        if c[1] == p:
            state[c] = []
            if c != from_ch:
                recording.add(c)
        if c[0] == p:
            ch[c].append("M")

def deliver(c):
    m = ch[c].popleft()
    if m == "M":
        if c[1] not in snap:
            start(c[1], from_ch=c)
        else:
            recording.discard(c)
    else:
        bal[c[1]] += m
        if c in recording:
            state[c].append(m)

def send(a, b, amt):
    bal[a] -= amt
    ch[(a, b)].append(amt)

send("P", "Q", 10)
send("Q", "P", 5)
start("P")
deliver(("Q", "P"))
deliver(("P", "Q"))
deliver(("P", "Q"))
deliver(("Q", "P"))
total = sum(snap.values()) + sum(sum(v) for v in state.values())
print("recorded process states:", snap)
print("recorded channel states:", {f"{a}->{b}": v for (a, b), v in state.items()})
print(f"snapshot total = {total} (initial total 150)")
```
```output
recorded process states: {'P': 90, 'Q': 55}
recorded channel states: {'Q->P': [5], 'P->Q': []}
snapshot total = 150 (initial total 150)
```
P recorded 90 after sending 10; its channel from Q recorded the in-flight 5; Q recorded 55 after receiving the 10, so the snapshot is 90 + 55 + 5 = 150. It is a state the system *could* have passed through, even though the real execution may never have been in exactly that state at one instant. Snapshots detect stable properties (deadlock, termination) and are the basis of checkpointing in stream processors such as Flink.

## 7.4 Distributed file systems

A **distributed file system** gives clients a file-system interface over files stored on servers. Design questions: naming, caching, consistency and failures.

**NFS (Network File System, Sun).** Clients mount a remote directory into the local tree. NFS v2/v3 servers are **stateless**: each request carries the file handle and offset, operations are **idempotent** (read, write at an offset), so a client simply retries after a lost reply (Unit 2) and a server reboot loses nothing. Clients cache blocks and attributes (about 3 to 30 seconds), so consistency is only **close-to-open**: data written by one client is guaranteed visible to another after the writer closes and the reader opens the file. NFSv4 adds state (locks, delegations) and strong security.

**AFS (Andrew File System).** Clients cache **whole files** on local disk; the server grants a **callback promise** and breaks it when another client updates the file, so cached copies are used with no server contact until invalidated. This scales to thousands of clients with **open-close (session) semantics**: a client sees the last file closed.

**GFS and HDFS** are designed for huge files, sequential reads, appends and commodity hardware that fails constantly. A single **master (NameNode)** keeps the namespace and block locations in memory and logs changes; files are split into large **chunks (blocks)** stored as replicas on **chunkservers (DataNodes)**. Clients ask the master where a block lives, then read or write directly to the servers, so data never flows through the master. GFS uses 64 MB chunks; HDFS defaults to **128 MB blocks** and replication factor **3**. DataNodes send **heartbeats** (every 3 seconds in HDFS) and block reports; missing heartbeats trigger **re-replication**. Replica placement is **rack-aware**: first replica on the writer's node, second on a node in a *different rack*, third on another node in the *same rack as the second*, trading write bandwidth for tolerance of a whole-rack failure. GFS also introduced **record append** with at-least-once semantics (duplicates and padding possible), a relaxed consistency model that applications handle. **MapReduce** runs computation next to this data: map tasks process local blocks, a shuffle groups values by key, and reduce tasks aggregate.

```python
import math
MB = 1024 ** 2
size, block, rep = 1000 * MB, 128 * MB, 3
blocks = math.ceil(size / block)
last = size - (blocks - 1) * block
print(f"{blocks} blocks (last block {last // MB} MB), {blocks * rep} replicas, raw storage {size * rep // MB} MB")
print(f"NameNode metadata at ~150 B per block: 100 million blocks = {100e6 * 150 / 1e9:.0f} GB")
N = 100
for k in (2, 3, 4):
    p = math.comb(k, 3) / math.comb(N, 3)
    print(f"{k} simultaneous node failures of {N}: P(a given block lost) = {p:.2e}")
racks = {"r1": ["a1", "a2", "a3"], "r2": ["b1", "b2", "b3"], "r3": ["c1", "c2", "c3"]}
def place(writer):
    r1 = next(r for r, ns in racks.items() if writer in ns)
    r2 = next(r for r in racks if r != r1)
    return [writer, racks[r2][0], racks[r2][1]]
print("replica placement for a write from a2:", place("a2"))
```
```output
8 blocks (last block 104 MB), 24 replicas, raw storage 3000 MB
NameNode metadata at ~150 B per block: 100 million blocks = 15 GB
2 simultaneous node failures of 100: P(a given block lost) = 0.00e+00
3 simultaneous node failures of 100: P(a given block lost) = 6.18e-06
4 simultaneous node failures of 100: P(a given block lost) = 2.47e-05
replica placement for a write from a2: ['a2', 'b1', 'b2']
```
A 1000 MB file occupies 8 blocks (the last only 104 MB) and 24 replicas, 3000 MB of raw disk. The NameNode keeps all metadata in RAM, which limits the number of files, not their size, and is why HDFS prefers a few large files to millions of small ones (a **standby NameNode** with a quorum journal removes the old single point of failure). If three nodes of a hundred fail at once, a given block is lost only if its three replicas are exactly those nodes: probability 1/C(100,3), about 6.18e-06. Two failures can never lose a 3-replica block.

## 7.5 Seeing failure: walls, disks, racks and snapshots

Failures are physical: disks that stop spinning, racks that lose power, and sometimes a component that lies. Plate 7.1 shows three pictures that give this unit its vocabulary, and Figures 7.1 to 7.3 show a Byzantine vote, a consistent snapshot and a distributed file system, each checked by a program.

```photogrid label="7.1" cols="3" ratio="1.0" caption="Failure in picture. (a) The Theodosian Walls of Constantinople: Lamport, Shostak and Pease named the Byzantine Generals problem (1982) after commanders of a besieging army, some of whom might be traitors, who must agree on a common plan by messenger. (b) The inside of a failed hard disk: the read-write arm rests beside the platter, and a disk that has crashed this way takes its data with it, which is why file systems keep several copies. (c) A rack of storage servers with rows of drive bays: a large cluster loses disks every day, so the software must treat failure as normal."
@ photo id="bca355/walls" cap="Theodosian Walls (Byzantium)"
fit 1.0
focus 0.5 0.55
@ photo id="bca355/hdfail" cap="Failed hard disk"
fit 1.0
focus 0.6 0.4
call 0.5 0.3 0.15 0.12 "read-write arm"
@ photo id="cs12/server-racks" cap="Rack of storage servers"
fit 1.0
focus 0.5 0.7
```

```svgfig label="7.1" caption="Byzantine agreement with four generals (f = 1 traitor, n = 3f + 1 = 4). The commander C is loyal and orders ATTACK. Lieutenant L3 is a traitor and tells the other lieutenants RETREAT. Each loyal lieutenant takes a majority of the three values it holds: L1 sees ATTACK from C, ATTACK from L2 and RETREAT from L3, so it decides ATTACK; L2 does the same. The oral-messages algorithm OM(1) sends 9 messages for n = 4."
f = Fig(580, 230)
f.box(240, 8, 100, 40, "Commander C\nloyal", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(40, 150, 110, 44, "L1 (loyal)\nsees A, A, R", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(235, 150, 110, 44, "L2 (loyal)\nsees A, A, R", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(430, 150, 120, 44, "L3 (traitor)\nsends R", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(260, 48), (110, 150)], color=NAVY); f.arrow([(290, 48), (290, 150)], color=NAVY); f.arrow([(320, 48), (480, 150)], color=NAVY)
f.arrow([(430, 172), (345, 172)], color=RED, dash=True)
f.arrow([(235, 186), (150, 186)], color=NAVY, dash=True)
f.arrow([(480, 194), (110, 206)], color=RED, dash=True)
f.text(185, 76, "ATTACK", size=10, color=NAVY, bold=True)
f.text(330, 100, "ATTACK", size=10, color=NAVY, bold=True)
f.text(285, 222, "L1 and L2 both decide ATTACK: agreement despite the traitor", size=10.5, color=TEAL, bold=True)
```

```svgfig label="7.2" caption="A Chandy-Lamport snapshot. Process A starts with Rs 600, B with Rs 400, and A sends Rs 200 to B. A records its state after sending (Rs 400) and sends a MARKER on the channel. B receives the marker before the money, so it records its state (Rs 400) and records the channel A to B as holding Rs 200. The snapshot total is 400 + 400 + 200 = Rs 1000, equal to the real total, though no instant ever had exactly these three values."
f = Fig(580, 200)
f.text(30, 54, "A", size=13, color=NAVY, bold=True)
f.text(30, 144, "B", size=13, color=NAVY, bold=True)
f.line(50, 50, 560, 50, color=SLATE, sw=1.4); f.line(50, 140, 560, 140, color=SLATE, sw=1.4)
f.circle(110, 50, 7, fill=BLUE, stroke=NAVY)
f.text(110, 30, "send Rs 200", size=10, color=NAVY, bold=True)
f.circle(190, 50, 8, fill=SAND, stroke=AMBER)
f.text(190, 30, "record A = 400", size=10, color=AMBER, bold=True)
f.arrow([(110, 50), (400, 140)], color=NAVY, sw=1.8)
f.arrow([(190, 50), (330, 140)], color=AMBER, sw=1.8, dash=True)
f.circle(330, 140, 8, fill=SAND, stroke=AMBER)
f.text(330, 168, "marker arrives first: record B = 400", size=10, color=AMBER, bold=True)
f.circle(400, 140, 7, fill=BLUE, stroke=NAVY)
f.text(450, 120, "money arrives: counted in channel", size=10, color=TEAL, bold=True, anchor="start")
f.text(290, 192, "snapshot: A 400 + B 400 + channel 200 = 1000", size=11, color=RED, bold=True)
```

```svgfig label="7.3" caption="A distributed file system in the HDFS style. The NameNode holds only metadata (file names and block locations, about 150 bytes per object, so 100,000,000 files with their blocks need about 30 GB of memory). The DataNodes hold 128 MB blocks, each copied to three nodes on two racks. A 1 GB file becomes 8 blocks and 24 stored replicas, using 3 GB of raw disk. Clients get block locations from the NameNode and then read data directly from the DataNodes."
f = Fig(580, 240)
f.box(200, 8, 180, 44, "NameNode (metadata)\nfile -> blocks -> nodes", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(10, 100, 270, 130, "", fill="#f8fafc", stroke=SLATE)
f.box(300, 100, 270, 130, "", fill="#f8fafc", stroke=SLATE)
f.text(145, 116, "Rack 1", size=10.5, color=NAVY, bold=True)
f.text(435, 116, "Rack 2", size=10.5, color=NAVY, bold=True)
f.box(24, 130, 112, 40, "DataNode 1\nB1  B2", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(154, 130, 112, 40, "DataNode 2\nB1  B3", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(24, 180, 112, 40, "DataNode 3\nB2  B3", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(314, 130, 112, 40, "DataNode 4\nB1  B3", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(444, 130, 112, 40, "DataNode 5\nB2", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(314, 180, 112, 40, "DataNode 6\nB2  B3", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(240, 52), (160, 100)], color=SLATE, dash=True); f.arrow([(340, 52), (420, 100)], color=SLATE, dash=True)
f.text(150, 74, "heartbeats, block reports", size=9, color=SLATE)
```

### 7.5.1 Eight reasons why fault tolerance matters and how it is achieved

1. **Failures are normal at scale.** A cluster with 1,000 disks and a 2% yearly failure rate loses about 20 disks a year. The software must keep working while hardware is replaced. Designing for failure is cheaper than hoping it will not happen.
2. **Replication protects data.** Keeping three copies means that a block is lost only if all three disks fail before the system makes a new copy. With a 12-hour repair window, the chance of that after one disk failure is about 7.5e-10. For the whole cluster this is roughly 1.5e-08 events per year.
3. **Availability depends on repair time.** Availability is MTBF divided by (MTBF + MTTR). With a mean time between failures of 1000 hours and a repair time of 4 hours it is 99.60%. Faster repair raises availability as surely as fewer failures do.
4. **Failure detection by heartbeats.** Nodes send small messages regularly, and a node that is silent for too long is declared dead. A short time-out detects failure quickly but can wrongly condemn a slow node. The designer must balance the two.
5. **Byzantine tolerance for untrusted parties.** When some nodes may lie, as in a blockchain or an interbank network, 3f + 1 nodes are needed to tolerate f faulty ones. For f = 1, 2, 3 the minimum is 4, 7 and 10 nodes. Most data-centre systems only assume crashes, which needs just 2f + 1.
6. **Checkpoints and snapshots.** A consistent snapshot, as in Figure 7.2, lets a long computation restart from a saved state instead of from the beginning. The recorded total is correct (Rs 1000) even though processes did not stop. This saves hours of work after a crash.
7. **Rack-aware placement.** A distributed file system puts replicas on different racks, so that the loss of a whole rack's power or switch does not remove all copies. Reads choose the nearest replica, which also saves network bandwidth. A government data centre or a university cluster would use the same idea.
8. **Self-healing.** When a DataNode stops sending heartbeats, the NameNode finds the blocks that now have only two copies and orders new copies to be made. The user sees nothing. This continuous repair is what makes cheap commodity disks usable for important data.

## Chapter summary

- Redundancy is the basis of fault tolerance; failure detectors suspect silent nodes by timeout; crash tolerance needs 2f + 1 replicas for majorities, Byzantine tolerance 3f + 1.
- OM(1) works for n = 4 and fails validity for n = 3 with one traitor; PBFT quorums are 2f + 1 of 3f + 1.
- Chandy–Lamport records a consistent global state (90 + 55 + 5 = 150 here); checkpointing avoids the domino effect when coordinated.
- NFS is stateless with close-to-open consistency; AFS caches whole files with callbacks; GFS/HDFS use a master plus large replicated blocks with rack-aware placement.

## Practice

1. Differentiate fault, error and failure.
2. How many replicas are needed to tolerate 2 crash failures with majority agreement? And 2 Byzantine failures?
3. Why can three generals with one traitor not reach agreement using oral messages?
4. In OM(1) with n = 4 and a traitor lieutenant, a loyal lieutenant receives 1 from the commander and relays 1 and 0. What does it decide?
5. Explain the domino effect and how coordinated checkpointing avoids it.
6. In the Chandy–Lamport algorithm, what does a process do on receiving its first marker?
7. Why is NFS (v3) called stateless and what advantage follows?
8. Compare the consistency of NFS and AFS.
9. A 700 MB file is stored in HDFS (128 MB blocks, replication 3). How many blocks and replicas, and what raw storage?
10. State HDFS's default replica placement for a client on a DataNode.

::: note Answers and worked solutions
**1.** A fault is the cause (a bad disk); an error is the incorrect internal state it produces; a failure is when the service deviates from its specification.
**2.** Crash: 2f + 1 = 5. Byzantine: 3f + 1 = 7.
**3.** A lieutenant hearing "attack" directly and "retreat" from the other lieutenant cannot tell whether the commander or the other lieutenant lies; both situations look the same, so a rule that works for one fails for the other.
**4.** Its votes are [1, 1, 0]: majority 1. It decides 1 (attack), which is the loyal commander's value.
**5.** With independent checkpoints, rolling back a process that received a message after the checkpoint of its sender forces the sender back, and so on, cascading to the start. Coordinated checkpointing saves a consistent set together, so rollback never cascades.
**6.** It records its own state, records that incoming channel as empty, sends a marker on all outgoing channels and starts recording the other incoming channels until their markers arrive.
**7.** The server keeps no per-client state between requests (each carries handle and offset), so a crashed and rebooted server resumes immediately and idempotent requests can simply be retried.
**8.** NFS: close-to-open with a time-limited cache so readers may see stale data for a few seconds. AFS: whole-file caching with callbacks, so cached data is valid until the server announces a change; open-close semantics.
**9.** 700 / 128 = 5.47, so 6 blocks (5 of 128 MB and one of 60 MB); 18 replicas; raw storage 2100 MB.
**10.** First replica on the writer's node, second in a different rack, third on another node in the second replica's rack.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain the Byzantine Generals problem and the condition n >= 3f + 1.**

*Introduction.* In a Byzantine failure a node may behave arbitrarily, including lying or sending different values to different nodes. The problem asks whether loyal nodes can still agree (section 7.2, Figure 7.1).

1. **Statement.** A commander sends an order to n - 1 lieutenants. Agreement requires that all loyal lieutenants obey the same order, and that they obey the commander's order if the commander is loyal.
2. **Bound.** With oral (unsigned) messages, agreement is possible if and only if n >= 3f + 1. For f = 1, 2, 3 the minimum n is 4, 7, 10.
3. **Why three are not enough.** With n = 3 and f = 1, a lieutenant who hears ATTACK from the commander and RETREAT from the other lieutenant cannot tell which of the two is the traitor.
4. **Algorithm OM(f).** The commander sends to all; each lieutenant relays what it received to the others, recursively f times, and each takes the majority. For n = 4, f = 1 this needs 9 messages; for n = 7, f = 2 it needs 156 messages.
5. **Practical form.** PBFT and blockchain protocols reduce the cost with signatures and quorums, but the 3f + 1 bound for nodes remains.

| f | Minimum nodes n = 3f + 1 | Quorum size 2f + 1 | OM(f) messages |
|---|---|---|---|
| 1 | 4 | 3 | 9 |
| 2 | 7 | 5 | 156 |
| 3 | 10 | 7 | 3609 |

*Conclusion.* Tolerating liars costs more nodes and many more messages than tolerating crashes, so Byzantine protocols are used only where trust is limited.

**Q2 (5 marks). Describe the Chandy-Lamport snapshot algorithm with an example.**

*Introduction.* A global snapshot records a state of all processes and channels that could have occurred, without stopping the system. It is used for checkpoints and for detecting stable properties such as deadlock (section 7.3, Figure 7.2).

1. **Initiate.** A process records its own state, then sends a MARKER on every outgoing channel.
2. **First marker.** A process that receives a marker for the first time records its own state, marks that channel as empty, and sends markers on all its outgoing channels.
3. **Later markers.** On every other incoming channel, it records the messages that arrive before that channel's marker. These are the messages in transit.
4. **Termination.** The snapshot is complete when every process has received a marker on every incoming channel.
5. **Example.** A starts with Rs 600 and B with Rs 400. A sends Rs 200 and then records Rs 400; B receives the marker first and records Rs 400; the channel holds Rs 200. Total 400 + 400 + 200 = Rs 1000, which equals the true total.

*Conclusion.* The snapshot may not match any real instant, but it is consistent: it is a cut that no message crosses backwards. Channels must be FIFO.

**Q3 (10 marks). Discuss fault tolerance in distributed systems and describe how a distributed file system such as HDFS achieves reliability. Compare NFS, GFS and HDFS.**

*Introduction.* A fault-tolerant system continues to work correctly although some components fail. It is judged by its dependability: availability, reliability, safety and maintainability. Availability is MTBF / (MTBF + MTTR), so with MTBF = 1000 h and MTTR = 4 h it is 99.60%.

*Types of failure.* Crash (a node stops), omission (a message is lost), timing (a reply is late), and arbitrary or Byzantine (the node misbehaves). Byzantine failures need n >= 3f + 1 nodes (Figure 7.1), crashes only 2f + 1.

*Techniques.* (1) Redundancy: information (checksums), time (retry), physical (replicas). (2) Failure detection by heartbeats and time-outs. (3) Recovery by checkpoints and logs, and consistent snapshots (Figure 7.2). (4) Masking by replication and voting.

*HDFS design (Figure 7.3).* A single NameNode keeps the namespace and block map in memory (about 150 bytes per object, so 100,000,000 files with blocks take about 30 GB). DataNodes store 128 MB blocks and report by heartbeat. A 1 GB file is split into 8 blocks; with replication factor 3 that means 24 replicas and 3 GB of raw disk. Placement puts the first replica on the writer's node and the others on a different rack. A lost replica is detected by missing heartbeats and recreated from the survivors. With 12-hour repair, the chance that a block loses all three copies after one failure is about 7.5e-10.

| Feature | NFS | GFS | HDFS |
|---|---|---|---|
| Design aim | share files on a LAN | huge files on commodity PCs | open-source GFS clone |
| Metadata | server | single master | single NameNode (with standby) |
| Unit of storage | file | 64 MB chunk | 128 MB block |
| Replication | none by default | 3 copies | 3 copies, rack-aware |
| Consistency | close-to-open | relaxed, append-friendly | write-once, append |
| Failure handling | server crash blocks clients | automatic re-replication | automatic re-replication |

*Conclusion.* Fault tolerance is achieved by redundancy, detection and recovery working together. A file system such as HDFS shows the pattern in practice: cheap, failing disks are made reliable by replication across racks and by constant self-repair.
