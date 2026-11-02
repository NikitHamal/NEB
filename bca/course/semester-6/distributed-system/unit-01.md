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
