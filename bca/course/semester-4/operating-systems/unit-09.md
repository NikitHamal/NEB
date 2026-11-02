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
