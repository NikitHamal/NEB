---
subject: Distributed System
grade: BCA Semester 6
unit: 1
title: Introduction, Goals, Architectures and Naming
hours: 7
area: BCA 355 · Distributed System · Unit 1
---

When you send money through a mobile wallet, one tap triggers work on a phone, a telecom gateway, a bank's servers, a fraud-detection service and a notification service, probably spread over several data centres. No single machine "is" the wallet. The wallet is a *behaviour* produced by many computers that talk only by sending messages, that fail independently, and that do not share a clock. This unit defines what a distributed system is, why we build them, what makes them hard, and how they are organised.

::: key What this unit gives you
- A working definition of a distributed system and the goals that justify one: resource sharing, transparency, openness, scalability and dependability.
- The eight fallacies of distributed computing and the quantitative reasoning (availability, latency) that replaces wishful thinking.
- Processes, threads and servers; naming, DNS and the Chord distributed hash table.
- System models: synchronous vs asynchronous, and the failure models (crash, omission, timing, Byzantine).
:::

## 1.1 What is a distributed system?

Tanenbaum and van Steen define a distributed system as *a collection of autonomous computing elements that appears to its users as a single coherent system*. Two ideas are packed into that sentence. **Autonomous elements** are nodes (computers, phones, containers) that each run their own program, have their own memory and fail on their own. **Single coherent system** means users should not need to know where the nodes are or how many there are. Leslie Lamport's joke captures the cost: "A distributed system is one in which the failure of a computer you didn't even know existed can render your own computer unusable."

Three characteristics follow from the definition and shape the whole subject:

1. **Concurrency.** Components run at the same time and compete for shared resources.
2. **No global clock.** Nodes coordinate only by exchanging messages; each has its own drifting clock (Unit 3).
3. **Independent failures.** Any node or link can fail, and a node often cannot tell a crashed peer from a slow one (Unit 7).

A *parallel* system (a multicore chip, a supercomputer with shared memory) is built for speed with reliable, fast communication. A distributed system is built for sharing, scale and availability, and must live with slow, unreliable communication. The two overlap in clusters, but the design problems differ.

## 1.2 Goals

**Resource sharing.** Files, printers, databases, compute and storage are made available across the network: the web, cloud storage, peer-to-peer file sharing.

**Transparency.** Hiding the distribution from users and programmers. The classic forms are summarised below; full transparency is neither possible nor always desirable (a mobile app must tolerate a dead network).

| Transparency | Hides | Example |
|---|---|---|
| Access | Differences in data representation and how a resource is accessed | Same file API for local and remote files |
| Location | Where a resource is | `https://example.com.np/` does not reveal the data centre |
| Migration | That a resource moved | A virtual machine moves between hosts |
| Relocation | Move while in use | Live migration during a video call |
| Replication | That copies exist | A CDN serves the nearest copy |
| Concurrency | That others share the resource | Two users editing a database safely |
| Failure | That a component failed and recovered | A retry hides a lost packet |

**Openness.** Interfaces are published and standard (HTTP, TCP/IP, REST, gRPC definitions), so independent parties can interoperate and extend the system. Separate **policy** from **mechanism**: a cache offers the mechanism; the policy (what to evict) is configurable.

**Scalability** along three axes: *size* (more users and resources), *geography* (users far apart, latency grows) and *administration* (many organisations). Techniques: **hiding latency** (asynchronous communication, move computation to the client), **partitioning** (split data and work: DNS zones, database shards) and **replication/caching** (copies near users, at the price of consistency problems).

**Dependability.** Availability, reliability, safety and maintainability, built with redundancy (Unit 7).

## 1.3 The eight fallacies

Peter Deutsch and colleagues at Sun listed assumptions that new distributed-system builders wrongly make:

1. The network is reliable.
2. Latency is zero.
3. Bandwidth is infinite.
4. The network is secure.
5. Topology does not change.
6. There is one administrator.
7. Transport cost is zero.
8. The network is homogeneous.

Each fallacy produces a class of bug: ignoring (1) gives programs that hang forever on a lost reply; ignoring (2) gives chatty protocols that make a hundred small calls; ignoring (4) gives plain-text credentials crossing the internet. Two small calculations show why the fallacies are expensive to ignore.

### Availability arithmetic

If a component is up a fraction *a* of the time, then *n* replicas of which any one suffices are all down with probability (1 − a)ⁿ, so **parallel availability = 1 − (1 − a)ⁿ**. If a request needs *n* services in a chain, all must be up: **serial availability = aⁿ**. Redundancy raises availability; depth lowers it.

```python
def parallel(a, n):
    return 1 - (1 - a) ** n

for n in (1, 2, 3):
    print(f"{n} replica(s) at 99%: {parallel(0.99, n) * 100:.4f}%")
chain = 0.999 ** 5
print(f"5 services in series at 99.9% each: {chain * 100:.4f}%")
print(f"downtime per year: {(1 - chain) * 365 * 24 * 60:.1f} minutes")
```
```output
1 replica(s) at 99%: 99.0000%
2 replica(s) at 99%: 99.9900%
3 replica(s) at 99%: 99.9999%
5 services in series at 99.9% each: 99.5010%
downtime per year: 2622.7 minutes
```
Three 99% replicas give "six nines" only if failures are independent; a shared power feed or a shared bad deploy breaks the assumption. A chain of five "three-nines" services is worse than any one of them: about 2622.7 minutes of downtime per year instead of 526.

### Latency arithmetic

Light in optical fibre travels at about 200,000 km/s, so a link of 2,000 km costs at least 10 ms one way no matter how fast the routers are:

```python
dist_km, speed = 2000, 200_000
one_way = dist_km / speed * 1000
rtt = 2 * one_way
print(f"one-way {one_way:.1f} ms, round trip {rtt:.1f} ms")
msg_bits = 1024 * 8
print(f"stop-and-wait: {1000 / rtt:.0f} msg/s = {1000 / rtt * msg_bits / 1000:.1f} kbit/s")
print(f"10 sequential remote calls cost {10 * rtt:.0f} ms; one batched call {rtt:.0f} ms")
```
```output
one-way 10.0 ms, round trip 20.0 ms
stop-and-wait: 50 msg/s = 409.6 kbit/s
10 sequential remote calls cost 200 ms; one batched call 20 ms
```
A protocol that sends one message and waits for the reply cannot exceed one message per round trip, however fat the pipe. This is why remote calls are batched, pipelined, cached or moved nearer to the user.

## 1.4 System architectures

**Client-server.** Clients request, servers respond. In a *two-tier* system the client holds the user interface and the server the data; in a *three-tier* system the interface, application logic and data live in separate tiers (browser, application server, database server). Tiers can be *physically* distributed; a single tier can be *vertically* replicated and *horizontally* partitioned across servers behind a load balancer.

**Peer-to-peer (P2P).** Every node is both client and server. No central server means no single point of failure and capacity that grows with the peers, but search, trust and consistency get harder.

- *Unstructured* overlays (Gnutella) connect peers randomly; a query is **flooded** to neighbours with a time-to-live (TTL). Simple and robust, but expensive and not guaranteed to find rare items.
- *Structured* overlays (Chord, Pastry, Kademlia) place each key on a node by a rule, so lookup takes O(log N) messages. These are **distributed hash tables** (DHTs); BitTorrent's trackerless mode uses Kademlia.
- *Hybrid:* a central index (early Napster) or super-peers keep search quick while data transfer is peer-to-peer.

**Middleware.** A layer between the operating system and applications that hides heterogeneity and offers common services: communication (RPC, messaging), naming, security, transactions, replication. Examples: CORBA, Java RMI, gRPC, Kafka, Kubernetes service discovery. The middleware is where most of the transparencies in the table above are implemented.

## 1.5 Processes, threads and servers

A **process** is a program in execution with its own address space; a **thread** is a unit of execution inside a process sharing its memory. Threads let a server overlap I/O waits with computation, and let a client fetch several web objects at once.

Server designs:

- **Iterative:** handles one request at a time. Simple, but a slow request blocks all.
- **Concurrent, thread-per-request or thread pool:** a dispatcher hands requests to workers. A pool bounds resource use; unlimited threads collapse under load.
- **Event-driven (single thread with asynchronous I/O):** Node.js, nginx. Very efficient for many idle connections; a blocking call stalls everything.

A server is **stateless** if it keeps no per-client information between requests (every request carries what the server needs). It is **stateful** if it remembers clients (open files, sessions). Stateless servers recover trivially from a crash and scale behind a load balancer; stateful servers are faster for some work but need recovery logic. Cookies and tokens move session state to the client.

**Code migration** moves a program (or part) to where the data is, as with JavaScript sent to the browser or a SQL query shipped to the database. **Virtualization** (virtual machines and containers) lets many isolated servers share hardware and makes migration easy; it is the foundation of cloud computing.

## 1.6 Naming and the Chord DHT

A **name** refers to an entity; an **address** is the name of an access point; an **identifier** is a unique, permanent name. Naming systems are of three kinds:

1. **Flat names** (random identifiers, MAC addresses): no location information, so the system needs a lookup mechanism such as broadcast, forwarding pointers, a home agent, or a DHT.
2. **Structured names:** human-readable, hierarchical (file paths, domain names).
3. **Attribute-based names:** entities found by properties (LDAP, service directories: "a printer that is colour and on floor 2").

**DNS** is the largest structured naming system: a tree of zones (root, `np`, `edu.np`, ...) each served by authoritative name servers, with *iterative* or *recursive* resolution and caching governed by TTLs. It illustrates partitioning (zones) and replication (secondary servers, caches) at once.

**Chord** gives flat names a decentralised lookup. Identifiers live on a ring of 2ᵐ positions; a key is stored on its **successor**, the first node clockwise from the key. Each node keeps a **finger table** with entries pointing to nodes 1, 2, 4, ..., 2^(m−1) positions ahead. To look up a key, a node forwards to the farthest finger that does not overshoot the key, which at least halves the remaining distance each step, so a lookup takes O(log N) hops. In a full ring of 16 nodes (m = 4), the hops from node 0 to a key at clockwise distance *d* are the number of 1-bits in *d*:

```python
M = 4
N = 2 ** M
def lookup(start, key):
    node, path = start, [start]
    while node != key:
        dist = (key - node) % N
        jump = 1 << (dist.bit_length() - 1)
        node = (node + jump) % N
        path.append(node)
    return path

for key in (13, 7, 15, 0):
    p = lookup(0, key)
    print(f"key {key:2d}: {' -> '.join(map(str, p))}  ({len(p) - 1} hops)")
total = sum(len(lookup(0, k)) - 1 for k in range(N))
print(f"average over all {N} keys: {total / N:.2f} hops (log2(N)/2 = {M / 2})")
```
```output
key 13: 0 -> 8 -> 12 -> 13  (3 hops)
key  7: 0 -> 4 -> 6 -> 7  (3 hops)
key 15: 0 -> 8 -> 12 -> 14 -> 15  (4 hops)
key  0: 0  (0 hops)
average over all 16 keys: 2.00 hops (log2(N)/2 = 2.0)
```
When a node joins or leaves, only the keys between it and its predecessor move, so churn is cheap. We reuse this idea as *consistent hashing* in the cloud-storage unit of the Cloud Computing book.

## 1.7 System models

Algorithms are designed against a **model** of the system.

- **Synchronous:** known bounds on message delay, processing time and clock drift. Failures can be detected with timeouts. Few real systems satisfy this.
- **Asynchronous:** no bounds. A slow node is indistinguishable from a crashed one. The **FLP result** (Fischer, Lynch, Paterson, 1985) proves that no deterministic algorithm can guarantee consensus in an asynchronous system if even one process may crash; practical protocols (Paxos, Raft) therefore guarantee safety always and liveness only when the network behaves for long enough.
- **Partially synchronous:** the system is asynchronous for unknown periods but eventually well-behaved. This is the usual realistic assumption.

**Failure models**, from mild to severe: **crash** (a process halts and stays halted), **omission** (messages or receive/send operations are lost), **timing** (a response arrives too late), **arbitrary or Byzantine** (a process behaves in any way, even maliciously). Tolerating Byzantine faults costs far more replicas than tolerating crashes (Unit 7).

## 1.8 Seeing distributed systems: hardware, architecture and numbers

A distributed system is software, but it lives on real machines in real halls: racks of servers, cards that put bits on a wire, cables that carry them. Plate 1.1 shows three of those physical pieces, and Figures 1.1 to 1.3 show how software arranges itself on them.

```photogrid label="1.1" cols="3" ratio="1.1" caption="The physical side of a distributed system. (a) A computer-centre hall at CERN holding the servers of the Worldwide LHC Computing Grid: thousands of ordinary machines in rows, each one a node, linked by a network so that scientists in many countries can share one pool of storage and processing. (b) A Fujitsu Primergy blade-server chassis: many thin server boards slide into one box that supplies power, cooling and network ports, which is how a data centre packs many nodes into little space. (c) A PCI Ethernet network interface card with its RJ-45 socket: every node reaches the others through such a card, and all of the delays, losses and failures of Section 1.3 begin at this interface."
@ photo id="bca355/lhc" cap="Server hall (CERN grid)"
fit 1.1
focus 0.5 0.5
call 0.55 0.75 0.45 0.55 "racks of nodes"
@ photo id="bca355/blade" cap="Blade-server chassis"
fit 1.1
focus 0.6 0.5
call 0.62 0.45 0.45 0.2 "server boards"
@ photo id="bca355/nic" cap="Ethernet network card"
fit 1.1
focus 0.45 0.5
call 0.28 0.55 0.2 0.3 "RJ-45 port"
```

```svgfig label="1.1" caption="A three-tier web architecture. Clients (phones and browsers) send requests to a load balancer, which spreads them across identical stateless application servers. The application servers read and write a primary database, which copies every change to a replica. The balancer hides the number of servers (replication and location transparency); the replica lets the data tier survive one crash (failure transparency)."
f = Fig(580, 266)
f.box(10, 95, 90, 60, "Clients\nphone, browser", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(130, 95, 90, 60, "Load\nbalancer", fill=SAND, stroke=AMBER, size=11, bold=True)
for i, y in enumerate((18, 95, 172)):
    f.box(265, y, 120, 60, "App server " + str(i + 1) + "\n(stateless)", fill=MINT, stroke=TEAL, size=10.5, bold=True)
    f.arrow([(220, 125), (265, y + 30)], color=SLATE)
    f.arrow([(385, y + 30), (440, 125)], color=SLATE)
f.arrow([(100, 125), (130, 125)], color=SLATE)
f.box(440, 60, 130, 50, "Primary database", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.box(440, 140, 130, 50, "Replica database", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(505, 110), (505, 140)], color=RED, dash=True)
f.text(530, 130, "copy", size=9, color=RED)
f.text(65, 252, "client tier", size=10, color=SLATE)
f.text(325, 254, "application tier", size=10, color=SLATE)
f.text(505, 252, "data tier", size=10, color=SLATE)
```

```svgfig label="1.2" caption="Why replicas raise availability but a long chain lowers it. Top: five services in series, each 99.9% available, give 0.999 to the power 5 = 99.5010%, about 2623 minutes of downtime a year. Bottom: two replicas in parallel, each only 99% available, give 1 - 0.01 x 0.01 = 99.99%, about 53 minutes a year."
f = Fig(580, 200)
f.text(290, 14, "Series: all must work, availabilities multiply", size=11, color=NAVY, bold=True)
for i in range(5):
    x = 20 + i * 108
    f.box(x, 26, 84, 40, "S" + str(i + 1) + "  99.9%", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
    if i < 4:
        f.arrow([(x + 84, 46), (x + 108, 46)], color=SLATE)
f.text(290, 86, "result = 99.5010%  (2623 min/year down)", size=11, color=RED, bold=True)
f.text(290, 114, "Parallel: one is enough, unavailabilities multiply", size=11, color=NAVY, bold=True)
f.box(150, 126, 110, 36, "Replica A  99%", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.box(320, 126, 110, 36, "Replica B  99%", fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.arrow([(100, 144), (150, 144)], color=SLATE); f.arrow([(260, 144), (320, 144)], color=SLATE, dash=True)
f.arrow([(430, 144), (480, 144)], color=SLATE)
f.text(290, 188, "result = 99.99%  (53 min/year down)", size=11, color=TEAL, bold=True)
```

```svgfig label="1.3" caption="A Chord ring with sixteen nodes (identifiers 0 to 15). A lookup for key 14 that starts at node 3 has distance (14 - 3) mod 16 = 11 = 1011 in binary. Each hop clears the largest remaining power of two: jump 8 to node 11, jump 2 to node 13, jump 1 to node 14. Three hops are needed, never more than log2(16) = 4."
import math
f = Fig(580, 260)
cx, cy, R = 200, 130, 100
pos = {}
for k in range(16):
    a = -math.pi / 2 + k * 2 * math.pi / 16
    pos[k] = (cx + R * math.cos(a), cy + R * math.sin(a))
path = [3, 11, 13, 14]
for u, v in zip(path, path[1:]):
    f.arrow([pos[u], pos[v]], color=RED, sw=2.2)
for k in range(16):
    x, y = pos[k]
    hot = k in path
    f.circle(x, y, 13, fill=(SAND if hot else BLUE), stroke=(RED if hot else NAVY), label=str(k), size=11)
f.box(370, 30, 200, 52, "start: node 3\nkey 14 lives at node 14", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(370, 95, 200, 52, "hop 1: 3 + 8 = 11\nhop 2: 11 + 2 = 13", fill=SAND, stroke=AMBER, size=10.5, bold=True)
f.box(370, 160, 200, 52, "hop 3: 13 + 1 = 14\nlookup finished in 3 hops", fill=MINT, stroke=TEAL, size=10.5, bold=True)
```

### 1.8.1 Eight applications of distributed systems

1. **Online payments.** A payment such as a Fonepay QR scan or a ConnectIPS transfer touches the customer's bank, the merchant's bank and a switch in between. These are separate organisations with separate computers, so no single machine can see the whole transaction. Atomic commit and careful retries make sure that money is neither lost nor taken twice.
2. **Government portals.** A service like the Nagarik App or a department's online form is used by people all over Nepal, from Kathmandu to Humla. The work is spread over several servers so that the portal still answers when one fails. Caches and replicas place copies of the data nearer to users, which cuts waiting time over slow links.
3. **Education records.** A national student-information system such as Tribhuvan University's EMIS or a college's result portal serves thousands of students at once, especially on result day. Many servers share the load, and a database replica holds a second copy of every mark. This is the scalability goal of this unit in a place every student knows.
4. **Weather and disaster data.** A forecast office such as the Department of Hydrology and Meteorology gathers readings from many stations in the hills and plains. Each station is a node that sends measurements by radio or mobile data, sometimes over unreliable links. The system must tolerate late, lost and duplicated messages and still give a correct picture.
5. **Search and the web.** A web search covers billions of pages, far more than one disk can hold. The index is split into shards on many machines and every query is sent to all of them at once, then the answers are merged. This is partitioning for size and parallelism for speed.
6. **Content delivery and video.** A video watched in Pokhara may come from a cache server much closer than the original in another country. Replicas of popular content are kept at the edge of the network. This hides the distance (location transparency) and reduces the load on the origin servers.
7. **Telecom and messaging.** A mobile network and a messaging app route millions of messages a minute through many switching nodes. Each node knows only its neighbours, and messages are queued if a link is down. Asynchronous message queues let the sender carry on without waiting for the receiver.
8. **Science and cloud computing.** Projects such as the CERN grid in Plate 1.1 join thousands of ordinary computers into one resource, and public clouds rent that kind of resource by the hour to anyone. A student in Biratnagar can start ten servers for an experiment and delete them afterwards. This sharing of resources is the first goal of a distributed system.

## Chapter summary

- A distributed system is autonomous nodes cooperating by messages to look like one system; it has concurrency, no global clock and independent failures.
- Goals: resource sharing, transparency (access, location, migration, replication, concurrency, failure), openness, scalability (size, geography, administration) and dependability.
- Serial availability multiplies (five 99.9% services give 99.5010%); parallel replicas raise it as 1 − (1 − a)ⁿ; latency is bounded by distance.
- Architectures: client-server (tiers), P2P (unstructured, structured DHT, hybrid); middleware hides heterogeneity.
- Chord places keys on a ring with O(log N) lookup; DNS combines partitioning and replication.
- Models: synchronous, asynchronous, partially synchronous; failures: crash, omission, timing, Byzantine. FLP forbids guaranteed deterministic consensus under asynchrony.

## Practice

1. Define a distributed system. Name three characteristics that distinguish it from a single computer.
2. List and give one example of five kinds of transparency.
3. Explain the difference between the scalability of size, geography and administration, with one technique for each.
4. State any four of the eight fallacies and the bug each one causes.
5. A service has two independent replicas, each 99.5% available. What is the availability of the pair?
6. A request passes through four services in series, each 99.95% available. What is the availability and the yearly downtime in minutes?
7. A link of 3,000 km in fibre (200,000 km/s). Find the round-trip propagation time and the maximum number of stop-and-wait messages per second.
8. In the Chord ring of 16 nodes, how many hops from node 3 to key 14? Use the bit-count rule.
9. Compare iterative, thread-pool and event-driven servers. When is each suitable?
10. Distinguish stateless and stateful servers. Which recovers more easily from a crash and why?
11. Why does the FLP result not prevent Paxos from being used in practice?

::: note Answers and worked solutions
**1.** A collection of autonomous computing elements that appears to its users as a single coherent system. It has concurrency, no global clock and independent failures.
**2.** Access (same API for local and remote files), location (a URL hides the server's place), replication (a CDN hides the copies), concurrency (a database isolates concurrent users), failure (a retry hides a lost packet).
**3.** Size: add users and resources, use partitioning (sharding). Geography: users far apart, use replication and caching near them. Administration: many organisations, use clear trust boundaries, federation and policies.
**4.** Reliable network: hangs on lost replies, so use timeouts and retries. Zero latency: chatty protocols, so batch. Secure network: plain-text passwords, so use TLS. One administrator: assumes one policy, but configurations conflict across organisations.
**5.** 1 − (0.005)² = 1 − 0.000025 = 99.9975%.
**6.** 0.9995⁴ = 99.8001%; downtime = 1050.4 minutes per year.
**7.** One way: 3,000/200,000 = 15 ms; round trip 30 ms; maximum 1000/30 = 33.3 messages per second.
**8.** Distance = (14 − 3) mod 16 = 11 = 1011 in binary, which has three 1-bits, so 3 hops (3 → 11 → 13 → 14).
**9.** Iterative: simple, low load only. Thread pool: moderate concurrency with blocking calls and bounded resources. Event-driven: many mostly idle connections; avoid blocking calls.
**10.** Stateless servers keep nothing between requests, so a restarted server or a different replica can serve the next request with no recovery step. Stateful servers must rebuild or lose the client state.
**11.** FLP forbids *guaranteed termination* under pure asynchrony. Paxos never violates safety (agreement and validity) and terminates whenever the system is eventually well-behaved, which real networks nearly always are.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q1 (5 marks). Explain transparency in a distributed system. Name and illustrate five kinds.**

*Introduction.* Transparency means hiding the fact that a system is spread over many computers, so that users and programmers see one coherent system (section 1.2).

1. **Access transparency.** The same operation is used for local and remote resources. For example, a program opens a file the same way whether it is on the local disk or on a network share.
2. **Location transparency.** Names do not show where a resource is. A web address does not tell the user which city holds the server.
3. **Replication transparency.** Several copies exist but look like one. A video served from a nearby cache server appears to be the same file as the original.
4. **Concurrency transparency.** Many users share a resource without interfering. A bank database lets thousands of people update accounts at the same time and gives each a consistent result.
5. **Failure transparency.** A fault is hidden from the user. If one server in Figure 1.1 crashes, the load balancer sends the request to another and the user sees only a slightly slower reply.

| Kind | What is hidden | Example |
|---|---|---|
| Access | local or remote | network file share |
| Location | where | URL |
| Replication | number of copies | CDN cache |
| Concurrency | sharing | database transactions |
| Failure | faults | load balancer retry |

*Limits.* Full transparency is impossible. The speed of light gives a 30 ms round trip over 15 ms of one-way fibre delay on a 3,000 km link, and a network partition cannot be hidden, so good designs aim at reasonable transparency and document the rest.

**Q2 (5 marks). Three services with availabilities 99.9%, 99.95% and 99.8% are used in series. Find the availability and yearly downtime. How much better is it with two replicas of each service?**

*Introduction.* For services in series, all must work, so availabilities multiply; for replicas in parallel, only one must work, so unavailabilities multiply (Figure 1.2).

1. **Series.** A = 0.999 x 0.9995 x 0.998 = 0.996503, which is 99.6503%.
2. **Downtime.** Unavailability is 0.003497, and a year has 525,600 minutes, so downtime is 1838 minutes, about 30.6 hours.
3. **With two replicas.** Each service becomes 1 - (1 - a)^2: for 99.9% it is 99.99990%; for 99.95% it is 99.999975%; for 99.8% it is 99.9996%.
4. **New chain.** The product is 99.9995%, so downtime falls to about 2.8 minutes a year.
5. **Conclusion.** Replication cuts downtime from hours to minutes, but only if failures are independent, so replicas must be on different machines, racks or sites.

**Q3 (10 marks). What is a distributed system? Describe its goals and compare the main architectures, with a diagram.**

*Introduction.* A distributed system is a collection of autonomous computers that cooperate by passing messages and appear to the user as one coherent system. Its three marks are concurrency, no global clock and independent failure. Examples are web search, online banking and the Nagarik App.

*Goals.* (1) Resource sharing: printers, files and compute are used by many. (2) Transparency: access, location, replication, concurrency and failure are hidden. (3) Openness: standard protocols let parts from different vendors work together. (4) Scalability: growth in size, geography and administration is handled by partitioning, replication and caching. (5) Dependability: availability, reliability, safety and security are kept even when parts fail.

*Architecture, with Figure 1.1.* In the client-server model, clients ask and servers answer; adding tiers separates presentation, application logic and data. In the peer-to-peer model every node is both client and server; unstructured networks find data by flooding, while structured ones such as Chord use a distributed hash table and find a key in at most log N hops (Figure 1.3). A hybrid model has a central index with peer-to-peer transfer.

*Challenges.* The eight fallacies (reliable network, zero latency, infinite bandwidth, secure network, fixed topology, one administrator, zero transport cost, homogeneous network) are false, and each wrong assumption causes a bug.

| Feature | Client-server | Peer-to-peer |
|---|---|---|
| Control | central server | none or shared |
| Scalability | server is a bottleneck | grows with the peers |
| Single point of failure | yes | no |
| Management | easy | hard |
| Typical use | web, banking | file sharing, Chord, blockchain |

*Numbers.* A chain of five 99.9% services is only 99.501% available, while two 99% replicas give 99.99%.

*Conclusion.* Distributed systems are chosen for sharing, growth and fault tolerance, and the price is complexity: designers must plan for partial failure, delay and disagreement from the start.
