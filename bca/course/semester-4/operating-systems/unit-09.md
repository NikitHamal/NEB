---
subject: Operating Systems
grade: BCA Semester 4
unit: 9
title: Distributed Operating Systems
hours: 4
area: BCA 251 · Operating Systems · Unit 9
---

Search for something on a website: your request is served by dozens of machines that you never see, yet the experience is of one fast computer. A **distributed operating system** manages a collection of independent computers connected by a network so that they appear to users as a single coherent system. This unit covers why we build them, how their hardware and software are classified, and the two basic problems they solve: communication (message passing, RPC) and time (clock synchronization).

::: key What this unit gives you
- Definition, advantages and disadvantages of distributed systems over centralized systems and independent PCs.
- Hardware and software concepts: multiprocessors and multicomputers; network, distributed and multiprocessor OS.
- Communication: message passing, remote procedure call.
- Processes in distributed systems; physical clock synchronization (Cristian, Berkeley) and Lamport's logical clocks.
:::

## 9.1 Introduction

A **distributed system** is a collection of independent computers that appears to its users as a single coherent system (Tanenbaum). Properties: no shared memory, no shared clock, communication only by messages, independent failures.

### Advantages over a centralized system

| Advantage | Explanation |
|---|---|
| **Economics** | many cheap microprocessors give a better price/performance ratio than one mainframe |
| **Speed** | combined computing power can exceed the biggest single machine |
| **Inherent distribution** | bank branches, ATMs and university campuses are naturally spread out |
| **Reliability** | if one machine fails the rest continue (fault tolerance, replication) |
| **Incremental growth** | add machines as the load grows |

### Advantages over independent PCs

Data sharing (one customer database for all branches); device sharing (printers, big disks); communication (e-mail, chat); flexibility in spreading the workload among free machines.

### Disadvantages

| Disadvantage | Explanation |
|---|---|
| **Software** | few good general programs; hard to design and debug |
| **Networking** | messages can be lost, delayed or reordered; saturation |
| **Security** | easier sharing also means easier unauthorised access |
| **Complexity of failures** | *partial* failures: one node or link down while others continue |

### Design goals (transparency)

A good distributed system hides its distribution: **access** transparency (same operations local or remote), **location** (names do not show where), **migration**, **replication**, **concurrency**, **failure**. Complete transparency is unattainable (the speed of light and network failures show through), so designers choose where to stop.

## 9.2 Hardware and software concepts

### Hardware

| Class | Memory | Coupling | Examples |
|---|---|---|---|
| **Multiprocessor** | shared memory, one address space | tight | multicore PC, SMP server |
| **Multicomputer** | each CPU has private memory; communicate by messages | loose | cluster of PCs, data-centre racks |

Interconnection can be a bus or a switched network (grid, hypercube).

### Software

| Type | Idea | Transparency | Scalability | Example |
|---|---|---|---|---|
| **Network OS (NOS)** | each machine runs its own OS; users know which machine they use (`ssh`, remote login, file transfer) | low | high | Windows file sharing, UNIX with NFS |
| **True distributed OS** | one system image; the OS decides where processes run | high | moderate | Amoeba, Plan 9, research systems |
| **Multiprocessor time-sharing OS** | one OS controls a shared-memory machine with one run queue | high | low | Linux SMP |
| **Middleware-based system** | a layer above NOS offers uniform services | medium–high | high | CORBA, web services, Kubernetes, Hadoop |

Most real "distributed systems" today are NOS plus middleware, since a fully transparent distributed kernel has proved hard to realise.

## 9.3 Communication in distributed systems

### Message passing

Processes on different machines exchange messages using `send(destination, message)` and `receive(source, message)`. Design choices:

- **Blocking (synchronous)** vs **non-blocking (asynchronous)** send; blocking receive.
- **Reliable vs unreliable**: use acknowledgements and retransmission (TCP) or accept loss (UDP).
- **Addressing**: process address, port or mailbox.
- **Buffering**: unbuffered (rendezvous) or with message queues.

Layered protocols: the application's message travels down through transport (TCP/UDP), network (IP) and link layers, as in the computer-network syllabus.

### Remote procedure call (RPC)

Message passing exposes I/O to the programmer. **RPC** (Birrell and Nelson, 1984) makes remote service look like a local procedure call: `result = add(3, 4)` runs on another machine.

**Steps** (client stub and server stub are generated code):

1. The client calls the local **client stub** as an ordinary procedure.
2. The stub **marshals** (packs) the parameters into a message and calls the OS to send it.
3. The client OS sends the message to the server machine.
4. The server OS passes it to the **server stub**.
5. The server stub **unmarshals** the parameters and calls the real server procedure.
6. The server runs and returns the result to its stub.
7. The server stub marshals the result and sends the reply message.
8. The client OS delivers it to the client stub, which unmarshals it and returns to the caller.

**Complications:** parameters cannot be pointers to the caller's memory (data must be copied: *call by copy/restore*); byte order and data formats differ (agree on a canonical format such as XDR or JSON/protobuf); and the **semantics of failure**: after a timeout the client cannot tell whether the request was lost, the server crashed before or after executing, or the reply was lost. Guarantees offered: *at-least-once* (retry; operation must be idempotent), *at-most-once* (sequence numbers, duplicate filtering) or the unattainable-in-general *exactly-once*.

::: example RPC versus local call
A local function call costs about 1 µs. An RPC in the same data-centre needs two network traversals of about 0.5 ms each, plus about 20 µs of stub and marshalling work: 2 × 500 + 20 = **1,020 µs**, about **1,000 times slower**. A design that makes one RPC with a list of 100 items is therefore far better than 100 RPCs with one item each.
:::

Modern equivalents are gRPC, REST-style HTTP APIs and JSON-RPC: the same pattern with newer encodings.

## 9.4 Processes and threads in distributed systems

Servers must handle many clients at once. Options: a **single-threaded** server (simple, but one slow request blocks all), a **multithreaded** server (a dispatcher thread hands each request to a worker thread: the best trade-off), or a **finite-state machine** (event-driven, non-blocking calls, as in Node.js and nginx). **Process migration** moves a running process to another machine to balance load; **code migration** moves code to the data. Clients are often thin: the user interface runs locally, the rest remotely; a **proxy** may cache or batch requests.

## 9.5 Clock synchronization

On a single machine, "A happened before B" is decided by one clock. In a distributed system every machine has its own crystal oscillator, which **drifts**: two clocks with a drift rate of 10⁻⁶ differ by up to 2 µs per second, or about 0.17 s per day. Without a common clock we must use algorithms.

### Physical clocks

- **Cristian's algorithm**: a client asks a time server for the time. If the request left at T₀, the reply arrived at T₁ and the server reported T_s, the client estimates the reply took half the round trip: **T_new = T_s + (T₁ − T₀) / 2**. Error is at most half the round trip.
- **Berkeley algorithm**: no machine has the true time. The coordinator **polls** every machine for its time, computes the **average** (ignoring outliers) and tells each machine the *adjustment* to make (not the new time), which avoids delay errors.
- **NTP (Network Time Protocol)**: hierarchy of servers (strata) tied to atomic clocks or GPS; typical accuracy is a few milliseconds over the Internet.

::: example Cristian and Berkeley, with numbers
**Cristian.** A client sends at T₀ = 0 ms and receives the reply at T₁ = 100 ms, which carries T_s = 550 ms. Round trip 100 ms, so the estimate is 550 + 100/2 = **600 ms**; the client sets its clock to 600 ms.

**Berkeley.** The coordinator's clock reads 3:00 and it polls A (3:25) and B (2:50). In minutes: 180, 205, 170, average = 555/3 = 185 = **3:05**. Adjustments sent: coordinator +5 min, A −20 min, B +15 min. All three then read 3:05. (Computed in `bca/tools/check_os_misc.py`.)
:::

### Logical clocks: Lamport's algorithm

For many purposes only the *order* of events matters, not real time. Lamport defined the **happened-before** relation (→): (1) if *a* and *b* are in the same process and *a* comes first, *a → b*; (2) if *a* is sending a message and *b* its receipt, *a → b*; (3) it is transitive. Events not related by → are **concurrent**.

**Lamport clock rules.** Each process keeps a counter *C*. (1) Before each event, *C = C + 1*. (2) A message carries the sender's *C*. (3) On receipt, *C = max(C, message timestamp) + 1*. If *a → b* then C(a) < C(b); the converse does not hold.

::: example Lamport timestamps
P1 has events a (clock 1), b (2), then sends message m₁ (3). P2 has event c (1); on receiving m₁ it sets C = max(1, 3) + 1 = **4**; then event d (5); it then sends m₂ (6). P1 receives m₂: C = max(3, 6) + 1 = **7**. Events c and a are concurrent (no message path), even though both have timestamp 1. **Vector clocks** (one counter per process) can detect concurrency exactly.
:::

### Other coordination problems

**Mutual exclusion** across machines uses a central coordinator (3 messages per entry), a distributed algorithm of Ricart and Agrawala (2(n − 1) messages) or a token ring; **election algorithms** (Bully, Ring) choose a new coordinator after a crash. These extend the single-machine ideas of Unit 3 to the network.

## 9.6 Seeing the ideas: nodes, clocks and message diagrams

A distributed system is made of ordinary machines, so the plate begins with real ones: a server node, a computing-grid hall, an atomic-clock apparatus and the computer scientist who defined logical time. The figures show the two hardware designs side by side, trace the eight steps of a remote procedure call, work Cristian's and Berkeley's clock algorithms with the numbers of this unit, and draw Lamport's timestamps on a message diagram.

```photogrid label="9.1" cols="4" ratio="1.0" caption="The pieces of a distributed system. (a) A Fujitsu PRIMERGY server node: one machine of many, with its own CPU, memory and operating system. (b) A computing-grid hall at CERN: thousands of such nodes joined by a network behave as one large system. (c) Louis Essen's caesium atomic clock apparatus: the kind of reference that time servers and NTP ultimately trace to. (d) Leslie Lamport, who defined the happened-before relation and logical clocks."
@ photo id="bca355/blade" cap="A server node"
fit 1.0
focus 0.6 0.5
call 0.53 0.5 0.04 0.9 "one node"
@ photo id="bca355/lhc" cap="Grid computing hall"
fit 1.0
focus 0.5 0.5
call 0.5 0.55 0.04 0.9 "many nodes"
@ photo id="bca355/essen" cap="Atomic clock apparatus"
fit 1.0
focus 0.5 0.5
call 0.5 0.55 0.04 0.9 "atomic clock"
@ photo id="bca355/lamport" cap="Leslie Lamport"
fit 1.0
focus 0.5 0.62
call 0.55 0.6 0.04 0.9 "logical time"
```

```svgfig label="9.1" caption="The two hardware designs. A multiprocessor (left) has several CPUs that share one memory and one address space, so processes communicate by reading and writing memory. A multicomputer (right) has nodes that each own a private memory, so the nodes communicate only by sending messages over a network. Clusters and data centres are multicomputers; a multicore laptop is a multiprocessor."
f = Fig(580, 210)
f.text(145, 14, "Multiprocessor (tightly coupled)", size=10.5, color=NAVY, bold=True)
f.text(435, 14, "Multicomputer (loosely coupled)", size=10.5, color=NAVY, bold=True)
for i in range(4):
    x = 14 + i * 66
    f.box(x, 30, 56, 34, "CPU %d" % (i + 1), fill=SAND, stroke=AMBER, size=10, bold=True)
    f.arrow([(x + 28, 64), (x + 28, 94)], color=SLATE, sw=1.4)
f.line(14, 96, 272, 96, color=NAVY, sw=3)
f.arrow([(143, 98), (143, 124)], color=TEAL, sw=1.6)
f.box(68, 124, 150, 34, "shared memory", fill=MINT, stroke=TEAL, size=10, bold=True)
f.line(290, 24, 290, 160, color="#cbd5e1", sw=1)
for i in range(3):
    x = 304 + i * 90
    f.box(x, 30, 80, 44, "node %d\nCPU + RAM" % (i + 1), fill=BLUE, stroke=NAVY, size=9.5, bold=True)
    f.arrow([(x + 40, 74), (x + 40, 104)], color=SLATE, sw=1.4)
f.line(304, 106, 566, 106, color=RED, sw=3)
f.text(435, 126, "network: messages", size=10, color=RED, bold=True)
f.text(145, 180, "one address space; talk through memory", size=10, color=TEAL, bold=True)
f.text(435, 180, "private memories; talk through messages", size=10, color=TEAL, bold=True)
f.text(290, 202, "unit 9 is about the right-hand design", size=10, color=SLATE)
```

```svgfig label="9.2" caption="The path of a remote procedure call. (1) The client calls its stub as if it were a local procedure. (2) The stub marshals the parameters into a message and asks the OS to send it. (3) The message crosses the network. (4) The server OS hands it to the server stub. (5) The server stub unmarshals the parameters and calls the real procedure. Steps 6 to 8 return the result the same way: the server stub marshals it, the server OS sends it, and the client stub unmarshals it and returns to the caller. The call looks local but costs about 1,020 microseconds against about 1 for a local call."
f = Fig(580, 240)
names = ["client\nprocess", "client\nstub", "client\nOS", "server\nOS", "server\nstub", "server\nprocedure"]
fills = [SAND, BLUE, SOFT, SOFT, BLUE, SAND]
edges = [AMBER, NAVY, SLATE, SLATE, NAVY, AMBER]
for i in range(6):
    x = 8 + i * 98
    f.box(x, 40, 72, 50, names[i], fill=fills[i], stroke=edges[i], size=9.5, bold=True)
for i in range(5):
    x1 = 8 + i * 98 + 72
    f.arrow([(x1, 56), (x1 + 26, 56)], color=TEAL, sw=1.6)
    f.arrow([(x1 + 26, 76), (x1, 76)], color=RED, sw=1.4, dash=True)
    f.text(x1 + 13, 50, str(i + 1), size=9.5, color=TEAL, bold=True)
f.text(290, 22, "teal arrows: request    red dashed arrows: reply (steps 6 to 8)", size=10, color=SLATE, bold=True)
steps = ["1  the client calls the stub like a local procedure",
         "2  the stub marshals the parameters; the OS sends the message",
         "3  the message crosses the network",
         "4  the server OS hands it to the server stub",
         "5  the stub unmarshals and calls the real procedure",
         "6-8  the result returns the same way: marshal, send, unmarshal"]
for i, s in enumerate(steps):
    f.text(40, 118 + i * 16, s, size=9.5, color=NAVY, anchor="start")
f.text(290, 232, "local call about 1 µs; RPC = 2 x 500 + 20 = 1,020 µs, about 1,000 times slower", size=10.5, color=RED, bold=True)
```

```svgfig label="9.3" caption="Two physical-clock algorithms with the numbers of this unit. Cristian (left): the client sends at T0 = 0 ms and receives the reply at T1 = 100 ms; the reply carries the server time Ts = 550 ms. The round trip is 100 ms, so the client sets its clock to Ts + (T1 - T0) / 2 = 550 + 50 = 600 ms. Berkeley (right): the coordinator reads 3:00 and polls A (3:25) and B (2:50). In minutes the clocks are 180, 205 and 170, average 555 / 3 = 185 = 3:05. The adjustments sent are +5, -20 and +15 minutes; all three then read 3:05."
f = Fig(580, 230)
f.text(145, 14, "Cristian's algorithm", size=10.5, color=NAVY, bold=True)
f.text(435, 14, "Berkeley algorithm", size=10.5, color=NAVY, bold=True)
f.line(290, 24, 290, 215, color="#cbd5e1", sw=1)
f.text(14, 56, "client", size=9.5, color=AMBER, bold=True, anchor="start")
f.line(60, 52, 260, 52, color=AMBER, sw=1.5)
f.text(14, 126, "server", size=9.5, color=TEAL, bold=True, anchor="start")
f.line(60, 122, 260, 122, color=TEAL, sw=1.5)
f.arrow([(70, 52), (125, 122)], color=NAVY, sw=1.6)
f.arrow([(125, 122), (180, 52)], color=RED, sw=1.6)
f.text(70, 38, "T0 = 0 ms", size=9.5, color=AMBER, bold=True)
f.text(180, 38, "T1 = 100 ms", size=9.5, color=AMBER, bold=True)
f.text(125, 140, "Ts = 550 ms", size=9.5, color=TEAL, bold=True)
f.text(145, 168, "round trip = 100 ms", size=10, color=SLATE)
f.text(145, 188, "T_new = 550 + 100 / 2 = 600 ms", size=10.5, color=RED, bold=True)
f.text(145, 206, "error at most half the round trip", size=9.5, color=SLATE)
boxes = [("coordinator\n3:00", 300), ("A\n3:25", 400), ("B\n2:50", 490)]
for tx, x in boxes:
    f.box(x, 30, 76, 44, tx, fill=BLUE, stroke=NAVY, size=10, bold=True)
adj = [("+5 min", 338, TEAL), ("-20 min", 438, RED), ("+15 min", 528, TEAL)]
for tx, cx, c in adj:
    f.arrow([(cx, 74), (cx, 120)], color=c, sw=1.5)
    f.text(cx, 136, tx, size=10.5, color=c, bold=True)
f.text(435, 98, "average = 555 / 3 = 185 min", size=9.5, color=NAVY, bold=True, anchor="middle")
f.text(435, 168, "= 3:05, sent as adjustments", size=10, color=NAVY, bold=True)
f.text(435, 188, "not as the new time", size=10, color=SLATE)
f.text(435, 206, "all three clocks now read 3:05", size=10.5, color=RED, bold=True)
```

```svgfig label="9.4" caption="Lamport timestamps on a message diagram. P1 has events a (clock 1), b (2) and sends m1 (3). P2 has event c (1); when m1 arrives it sets C = max(1, 3) + 1 = 4, then runs d (5) and sends m2 (6). P1 receives m2 and sets C = max(3, 6) + 1 = 7. If a happened before b then C(a) < C(b), but the converse is false: a and c both have clock 1 and no message path joins them, so they are concurrent."
f = Fig(580, 216)
f.text(14, 54, "P1", size=11, color=NAVY, bold=True, anchor="start")
f.text(14, 144, "P2", size=11, color=NAVY, bold=True, anchor="start")
f.line(40, 50, 565, 50, color=SLATE, sw=1.4)
f.line(40, 140, 565, 140, color=SLATE, sw=1.4)
f.arrow([(262, 50), (338, 140)], color=RED, sw=1.6)
f.arrow([(438, 140), (498, 50)], color=RED, sw=1.6)
p1 = [(100, 1, "a"), (180, 2, "b"), (260, 3, "send m1"), (500, 7, "recv m2")]
p2 = [(110, 1, "c"), (340, 4, "recv m1"), (390, 5, "d"), (440, 6, "send m2")]
for x, c, nm in p1:
    f.circle(x, 50, 13, fill=SAND, stroke=AMBER, label=str(c), size=10)
    f.text(x, 22, nm, size=9.5, color=AMBER, bold=True)
for x, c, nm in p2:
    f.circle(x, 140, 13, fill=MINT, stroke=TEAL, label=str(c), size=10)
    f.text(x, 172, nm, size=9.5, color=TEAL, bold=True)
f.text(290, 194, "on receive: C = max(C, timestamp) + 1  ->  max(1, 3) + 1 = 4 and max(3, 6) + 1 = 7", size=10, color=NAVY, bold=True)
f.text(290, 210, "a and c are concurrent: equal clocks, no message path", size=9.5, color=SLATE)
```

### 9.6.1 Eight advantages of distributed systems

1. **Economy.** Many cheap microprocessors give a better price for each unit of computing than one huge mainframe. A college can build a lab cluster from ordinary PCs instead of buying a supercomputer. When prices fall, the cluster can be renewed machine by machine.
2. **Speed through parallel work.** Many machines can work on parts of one job at the same time, so the total power can exceed any single computer. A search over millions of web pages is split among thousands of nodes and answered in a fraction of a second. A university can mark thousands of answer sheets faster by sharing the data among machines.
3. **Natural distribution.** Many real tasks are spread over many places. Bank branches, ATMs and mobile wallets such as Fonepay and eSewa serve customers in every district of Nepal. A distributed design puts the service close to the users instead of forcing everyone to travel to one computer.
4. **Reliability and fault tolerance.** When one machine fails, the others continue, especially if data is replicated. A banking system with copies in two cities keeps working if one data centre loses power. Users see a short delay instead of a complete stop.
5. **Incremental growth.** Capacity is added by putting in one more node as the load grows. A college portal can start with two servers during the admission season and add more for the result day. There is no need to replace the whole system.
6. **Data and device sharing.** Many users can read the same database and use the same expensive printers and large disks. A national system such as the Nagarik App or a university's EMIS depends on shared records. Everyone sees the same current data instead of separate stale copies.
7. **Communication and collaboration.** Distributed systems make email, chat, video classes and shared documents possible. Students in different towns can work on one project file at the same time. The OS and the network deliver the messages, so the users do not need to know where the others are.
8. **Flexibility in placing the work.** The load can be moved to machines that are idle, nearer to the data, or cheaper. A heavy report can run overnight on spare lab computers. Transparency hides these moves, so a user sees one system, though the cost is more complex software and failure handling.

## Formula and fact sheet

- Cristian: **T_new = T_s + (T₁ − T₀)/2**. Berkeley: adjustment = average − own time.
- Lamport: *C = C + 1* per event; on receive *C = max(C, t) + 1*; a → b ⇒ C(a) < C(b).
- Drift: a clock with drift ρ gains or loses ρ seconds per second.
- RPC cost ≈ 2 × network latency + stub time ≫ local call.
- Multiprocessor = shared memory; multicomputer = message passing.

## Chapter summary

- A distributed system is independent computers that look like one; it gives economy, speed, reliability and growth at the price of complexity, networking and security problems.
- Hardware divides into multiprocessors and multicomputers; software into network OS, distributed OS and middleware.
- Message passing and RPC are the basic communication tools; RPC hides messaging but not failures or latency.
- Clocks drift, so Cristian's and Berkeley's algorithms and NTP synchronise physical clocks, while Lamport clocks give a consistent order of events.

## Practice

1. Define a distributed system. List three advantages over a centralized system and three disadvantages.
2. Compare network operating systems and distributed operating systems.
3. Differentiate multiprocessors and multicomputers.
4. Describe the eight steps of an RPC. What problems does passing pointers cause?
5. Why can't a client always know whether an RPC executed? Explain at-least-once and at-most-once.
6. A client sends a request at T₀ = 10:00:00.000 and receives the reply at T₁ = 10:00:00.200, with server time 10:00:05.300 in the reply. What time should it set?
7. Clocks read 10:00, 10:10 and 09:50. Apply the Berkeley algorithm. What adjustments are sent?
8. Process P1: events a, then send m to P2; P2: event c, receive m, event d. Assign Lamport timestamps.
9. Why are Lamport timestamps not sufficient to detect concurrency?
10. Explain why a multithreaded server design is usually better than single-threaded.

::: note Answers and worked solutions
**1.** A set of independent computers appearing as one coherent system. Advantages: price/performance, reliability through replication, incremental growth. Disadvantages: complex software, network problems, security exposure.
**2.** NOS: each node has its own OS and users know about remote machines; simple, scalable, low transparency. Distributed OS: a single system image; the OS places processes and files transparently; harder to build.
**3.** A multiprocessor has several CPUs sharing one memory and one address space (multicore PC). A multicomputer has separate memories per CPU, communicating by messages (cluster).
**4.** Steps are listed in 9.3. Pointers are meaningless on the server, which has a different address space, so the data they refer to must be copied (copy/restore) or sent by value, which is costly and changes semantics for shared structures.
**5.** The request, the server, or the reply can fail, and the client sees only a timeout. At-least-once: retry until a reply, so the operation may run more than once and should be idempotent. At-most-once: the server keeps request IDs and filters duplicates, so the operation runs at most one time.
**6.** RTT = 200 ms; one-way ≈ 100 ms. New time = 10:00:05.300 + 0.100 = **10:00:05.400**.
**7.** In minutes after 09:00: 60 (10:00), 70, 50. Average = 180/3 = 60 → **10:00**. Adjustments: first machine 0, second **−10 min**, third **+10 min**.
**8.** P1: a = 1, send = 2. P2: c = 1, receive = max(1, 2) + 1 = 3, d = 4.
**9.** If a → b then C(a) < C(b), but C(a) < C(b) does not imply a → b: two concurrent events can have ordered timestamps. Vector clocks capture the exact relation.
**10.** With one thread, a request that waits on the disk or network blocks every other client. With a thread per request (or a pool), other requests proceed during the wait, and multiple cores can be used.
:::

## Model answers (5 and 10 marks)

**Q1. What is a distributed system? State its advantages and disadvantages over a centralized system. (5 marks)**

A **distributed system** is a collection of independent computers that appears to its users as a single coherent system. Its nodes have no shared memory and no shared clock, they communicate only by messages, and they can fail independently.

**Advantages over a centralized system:**

- **Economics**: many cheap microprocessors give a better price/performance ratio than one mainframe.
- **Speed**: the combined power can exceed that of the largest single machine.
- **Inherent distribution**: banks, ATMs and campuses are naturally spread out.
- **Reliability**: when a node fails the rest continue, especially with replication.
- **Incremental growth**: add machines as the load grows.

**Disadvantages:**

- **Software**: few good general programs; design and debugging are hard.
- **Networking**: messages can be lost, delayed or reordered, and the network can saturate.
- **Security**: easier sharing also makes unauthorised access easier.
- **Partial failures**: one node or link may be down while the others run, which is hard to detect and handle.

| Point | Centralized | Distributed |
|---|---|---|
| Growth | replace the machine | add nodes |
| Failure | whole system stops | partial failure |
| Cost | rises steeply | rises gradually |
| Complexity | low | high |

A distributed system is worth the extra complexity when scale and availability matter, as in a national banking network.

**Q2. Distinguish between a multiprocessor and a multicomputer, and between a network OS, a distributed OS and middleware. (5 marks)**

**Hardware (Figure 9.1).** A **multiprocessor** has several CPUs sharing one memory and one address space; coupling is tight and communication is by reading and writing memory (a multicore PC or SMP server). A **multicomputer** has nodes with private memories that communicate only by messages over a network; coupling is loose (a cluster or data-centre rack).

**Software.**

| Type | Idea | Transparency | Example |
|---|---|---|---|
| **Network OS** | each machine runs its own OS; users know which machine they use (`ssh`, file transfer) | low | Windows file sharing, UNIX with NFS |
| **True distributed OS** | one system image; the OS decides where processes run | high | Amoeba, Plan 9 |
| **Middleware-based** | a layer above a network OS gives uniform services | medium to high | web services, Kubernetes, Hadoop |

Most real systems today are a network OS plus middleware, because a fully transparent distributed kernel proved hard to build. The goal of the middleware is *transparency*: access, location, migration, replication, concurrency and failure are hidden from the user.

**Q3. What is a remote procedure call? Explain the steps of an RPC and the problems it raises. (10 marks)**

**Introduction.** Message passing with `send` and `receive` exposes input and output to the programmer. A **remote procedure call** (Birrell and Nelson, 1984) hides this by making a service on another machine look like an ordinary local procedure call, for example `result = add(3, 4)`.

**Steps (Figure 9.2).** The client stub and the server stub are generated code.

1. The client calls the local **client stub** as an ordinary procedure.
2. The stub **marshals** (packs) the parameters into a message and calls the OS to send it.
3. The client OS sends the message across the network to the server machine.
4. The server OS passes the message to the **server stub**.
5. The server stub **unmarshals** the parameters and calls the real server procedure.
6. The procedure runs and returns its result to the server stub.
7. The server stub marshals the result and the server OS sends the reply.
8. The client OS delivers it to the client stub, which unmarshals it and returns to the caller.

**Problems.**

- **Pointers and parameter passing.** A pointer into the caller's memory means nothing on the server, so data is copied (call by copy/restore).
- **Data representation.** Machines differ in byte order and formats, so a canonical encoding such as XDR, JSON or protobuf is agreed.
- **Failure semantics.** After a timeout the client cannot tell whether the request was lost, the server crashed before or after executing, or only the reply was lost. Hence systems offer *at-least-once*, *at-most-once* or *exactly-once* semantics, and operations should be **idempotent** where possible.
- **Cost.** A local call takes about 1 µs. A call in the same data centre needs two network traversals of about 500 µs each plus about 20 µs of stub work: 2 × 500 + 20 = **1,020 µs**, roughly 1,000 times slower.

| Point | Local call | RPC |
|---|---|---|
| Parameters | pointers allowed | copied values |
| Failure | both succeed or both fail | partial failure possible |
| Cost | about 1 µs | about 1,020 µs |

**Conclusion.** RPC makes distributed programs easier to write, but it hides neither latency nor failure; a good design makes few calls, each carrying a batch of work. gRPC and REST over HTTP are modern forms of the same pattern.

**Q4. Explain physical clock synchronization with Cristian's algorithm, the Berkeley algorithm and NTP. Work a numerical example of each. (10 marks)**

**Introduction.** Every machine has its own crystal oscillator, which **drifts**: with a drift rate of 10⁻⁶ two clocks can differ by 2 µs every second, about 0.17 s a day. Without correction, timestamps on different machines cannot be compared, which breaks logs, file timestamps and transactions.

**1. Cristian's algorithm.** A client asks a **time server** for the time. If the request left at T₀, the reply arrived at T₁ and the server reported T_s, the client assumes the reply took half of the round trip:

**T_new = T_s + (T₁ − T₀) / 2**

The error is at most half the round trip. *Example (Figure 9.3):* T₀ = 0 ms, T₁ = 100 ms and T_s = 550 ms give 550 + 100/2 = **600 ms**, so the client sets its clock to 600 ms.

**2. Berkeley algorithm.** No machine has the true time. The coordinator **polls** every machine, computes the **average** (ignoring outliers) and sends each machine the *adjustment* to make, not the new time, so message delay does not matter. *Example:* the coordinator reads 3:00, A reads 3:25 and B reads 2:50. In minutes the clocks are 180, 205 and 170 with average 555 / 3 = 185, which is **3:05**. The adjustments are coordinator **+5**, A **−20** and B **+15** minutes, and all three then read 3:05.

**3. NTP.** The Network Time Protocol uses a hierarchy of servers called **strata**: stratum 0 are atomic clocks or GPS receivers, stratum 1 servers are attached to them, and each lower stratum synchronises from the one above. Over the Internet it reaches an accuracy of a few milliseconds.

| Algorithm | True time source | What is sent | Error source |
|---|---|---|---|
| Cristian | one time server | the time itself | asymmetric delay, at most half the round trip |
| Berkeley | none (average) | adjustments | outliers and polling delay |
| NTP | atomic clock or GPS hierarchy | timestamps | network jitter, a few ms |

**Conclusion.** Cristian's algorithm fits when a reliable time server exists; Berkeley's fits an internal group with no external reference; NTP serves the whole Internet. When only the *order* of events matters, Lamport's logical clocks avoid the problem altogether.

**Q5. Explain Lamport's logical clocks with an example. (5 marks)**

For many tasks only the **order** of events matters, not the real time. Lamport defined the **happened-before** relation (→): (1) if *a* and *b* are in the same process and *a* comes first, then *a → b*; (2) if *a* sends a message and *b* receives it, then *a → b*; (3) the relation is transitive. Two events with no path between them are **concurrent**.

**Rules.** Each process keeps a counter *C*. (1) Before each event, *C = C + 1*. (2) A message carries the sender's *C*. (3) On receipt, *C = max(C, timestamp) + 1*. If *a → b* then C(a) < C(b).

**Example (Figure 9.4).** P1 has events a (1) and b (2) and sends m₁ with timestamp 3. P2 has event c (1); on receiving m₁ it sets C = max(1, 3) + 1 = **4**, runs d (5) and sends m₂ with timestamp 6. P1 receives m₂ and sets C = max(3, 6) + 1 = **7**.

The converse does not hold: a and c both have clock 1 but are concurrent, so a smaller timestamp does not prove that an event happened first. Lamport clocks give a consistent order for mutual exclusion and replicated databases without any physical clock.
