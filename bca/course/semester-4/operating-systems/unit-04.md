---
subject: Operating Systems
grade: BCA Semester 4
unit: 4
title: Deadlocks
hours: 4
area: BCA 251 · Operating Systems · Unit 4
---

Two programs each hold a resource the other needs and each waits politely for the other to let go. Neither ever will. This is a **deadlock**, and it is among the most examined topics in the OS paper: definitions, the four conditions, prevention, avoidance with the Banker's algorithm, detection and recovery.

::: key What this unit gives you
- System model and resource types; the four necessary conditions for deadlock.
- Deadlock modelling with resource-allocation graphs; the ostrich algorithm.
- Prevention, avoidance (safe states, the Banker's algorithm with a full worked example), detection and recovery.
:::

## 4.1 System model and resources

A system has a finite set of **resource types** (CPU cycles, memory pages, printers, files, semaphores), each with one or more identical **instances**. A process uses a resource in three steps: **request**, **use**, **release**. If the resource is not available at the request, the process waits.

| Resource kind | Meaning | Example | Deadlock-prone? |
|---|---|---|---|
| **Preemptable** | can be taken away without harm | CPU, memory (swapped out) | no |
| **Non-preemptable** | taking it back makes the computation fail | printer mid-job, tape, a locked file | yes |

Deadlocks of interest involve non-preemptable resources. Memory-type resources can be resolved by swapping.

::: definition Deadlock
A set of processes is **deadlocked** if each process in the set is waiting for an event (typically a resource release) that only another process in the set can cause.
:::

### Conditions for resource deadlocks (Coffman, 1971)

All four must hold at once:

1. **Mutual exclusion**: at least one resource is held in a non-sharable mode.
2. **Hold and wait**: a process holds one resource while waiting for another.
3. **No preemption**: a resource can be released only voluntarily by the holder.
4. **Circular wait**: there is a cycle P₀ → P₁ → … → Pₙ → P₀ where each process waits for a resource held by the next.

::: note Necessary, not sufficient
All four conditions are *necessary*. If any one is impossible, deadlock cannot occur; but all four together do not by themselves prove a deadlock exists (with multiple instances a cycle may be harmless).
:::

## 4.2 Deadlock modelling: the resource-allocation graph

A **resource-allocation graph (RAG)** has process nodes (circles), resource nodes (rectangles with a dot per instance), **request edges** P → R and **assignment edges** R → P.

- If the graph has **no cycle**, there is no deadlock.
- If it has a cycle and **every resource type has one instance**, a deadlock exists.
- If it has a cycle and resource types have **several instances**, a deadlock *may* exist.

::: example The classic two-process deadlock
P1 holds R1 and requests R2; P2 holds R2 and requests R1. Edges: R1 → P1, P1 → R2, R2 → P2, P2 → R1. That is the cycle R1 → P1 → R2 → P2 → R1 and both resources have one instance, so P1 and P2 are deadlocked. In code: thread A locks `m1` then `m2`; thread B locks `m2` then `m1`. If each gets its first lock before either takes its second, both wait forever.
:::

Deadlock depends on timing: with a different interleaving (A locks both before B starts) the same program finishes normally. That is why deadlocks are intermittent and hard to debug.

## 4.3 The ostrich algorithm and methods of handling deadlocks

There are four strategies:

| Strategy | Idea | Cost |
|---|---|---|
| **Ignore (ostrich algorithm)** | pretend deadlocks never happen; reboot or kill when a user complains | none up front; UNIX and Windows choose this for general resources |
| **Prevention** | design so that at least one of the four conditions can never hold | restricts resource use |
| **Avoidance** | the OS uses advance information and grants a request only if the state stays safe | needs maximum claims; run-time work |
| **Detection and recovery** | allow deadlock, detect it, then recover | detection cost; recovery loses work |

The **ostrich algorithm** is a legitimate engineering decision: if deadlocks occur once in several years but prevention would reduce performance every day, ignoring is rational. It is not acceptable in safety-critical systems.

## 4.4 Deadlock prevention

Attack each condition:

| Condition attacked | Technique | Drawback |
|---|---|---|
| Mutual exclusion | make resources sharable where possible (read-only files); **spooling** a printer so no process holds it directly | some resources are inherently non-sharable |
| Hold and wait | a process must request **all** resources before starting, or release everything before asking for more | low utilisation; starvation; future needs may be unknown |
| No preemption | if a request cannot be granted, the process **releases** what it holds and restarts; or the OS preempts from a waiting process | works only for state that can be saved (CPU, memory) |
| **Circular wait** | impose a **global ordering** on resource types; a process must request in increasing order | ordering may not suit all programs; the practical favourite |

Ordering works because a cycle would need some process to request a lower-numbered resource while holding a higher one, which the rule forbids. This is the same trick as the dining-philosophers fix in Unit 3: always lock the lower-numbered lock first.

## 4.5 Deadlock avoidance

### Safe and unsafe states

The OS needs to know each process's **maximum claim**. A state is **safe** if there exists some order of the processes, a **safe sequence** ⟨P₁, …, Pₙ⟩, such that each Pᵢ's remaining needs can be met by the available resources plus those held by all earlier Pⱼ (j < i), which will have finished and released theirs. If no such order exists the state is **unsafe**.

Safe ⇒ no deadlock. Unsafe ⇏ deadlock (processes might release resources in time), but an unsafe state *may* lead to deadlock, so avoidance never enters one.

### Resource-allocation graph algorithm (single instances)

Add **claim edges** Pᵢ ⇢ Rⱼ (dashed) showing future requests. A request is granted only if converting its claim edge to an assignment edge does not create a cycle.

### The Banker's algorithm (multiple instances)

Dijkstra's Banker's algorithm models a bank that never lends so much that it cannot satisfy all customers' maximum needs. With *n* processes and *m* resource types:

- `Available[j]` free instances of resource *j*;
- `Max[i][j]` maximum demand of process *i*;
- `Allocation[i][j]` currently held;
- `Need[i][j] = Max[i][j] − Allocation[i][j]`.

**Safety algorithm.** (1) Work = Available; Finish[i] = false for all *i*. (2) Find an *i* with Finish[i] = false and Need[i] ≤ Work. (3) Work = Work + Allocation[i]; Finish[i] = true; go to (2). (4) If all Finish[i] are true the state is safe.

**Resource-request algorithm** for a request Requestᵢ by process *i*: (1) if Requestᵢ > Needᵢ, error (exceeded its claim); (2) if Requestᵢ > Available, the process must wait; (3) pretend to allocate: Available −= Requestᵢ, Allocationᵢ += Requestᵢ, Needᵢ −= Requestᵢ; run the safety algorithm; if safe, the request is granted, otherwise it is rolled back and the process waits.

::: example Banker's algorithm, full worked example
Three resource types A, B, C with 10, 5 and 7 instances. Five processes:

| Process | Allocation (A B C) | Max (A B C) | Need = Max − Allocation | 
|---|---|---|---|
| P0 | 0 1 0 | 7 5 3 | 7 4 3 |
| P1 | 2 0 0 | 3 2 2 | 1 2 2 |
| P2 | 3 0 2 | 9 0 2 | 6 0 0 |
| P3 | 2 1 1 | 2 2 2 | 0 1 1 |
| P4 | 0 0 2 | 4 3 3 | 4 3 1 |

Total allocated = (7, 2, 5), so **Available = (10, 5, 7) − (7, 2, 5) = (3, 3, 2)**.

**Is the state safe?** Work = (3, 3, 2). P0 needs (7, 4, 3) > Work: skip. P1 needs (1, 2, 2) ≤ Work: run it, Work = (3, 3, 2) + (2, 0, 0) = **(5, 3, 2)**. P0 still too big (7 > 5); P2 needs (6, 0, 0) > 5: skip. P3 needs (0, 1, 1) ≤ Work: Work = (5, 3, 2) + (2, 1, 1) = **(7, 4, 3)**. Now P0 (7, 4, 3) ≤ (7, 4, 3): Work = **(7, 5, 3)**. P2 (6, 0, 0): Work = **(10, 5, 5)**. P4 (4, 3, 1): Work = **(10, 5, 7)**, which equals the total, as it must.

Safe sequence found by scanning from P0: **⟨P1, P3, P0, P2, P4⟩**. Another valid one is ⟨P1, P3, P4, P0, P2⟩; safe sequences are not unique.

**Request 1: P1 asks for (1, 0, 2).** (1, 0, 2) ≤ Need₁ (1, 2, 2) and ≤ Available (3, 3, 2). Pretend: Available = (2, 3, 0), Allocation₁ = (3, 0, 2), Need₁ = (0, 2, 0). The safety algorithm still finds ⟨P1, P3, P0, P2, P4⟩, so the request is **granted**.

**Request 2: P4 asks for (3, 3, 0)** in the *original* state. It is within Need₄ (4, 3, 1) and Available (3, 3, 2), so the algorithm pretends: Available = (0, 0, 2). No process's Need fits in (0, 0, 2) (P3 needs (0, 1, 1)), so the state is unsafe and the request is **denied** even though resources exist.

**Request 3: P0 asks for (0, 2, 0).** From the original state it leaves Available = (3, 1, 2), which still has a safe sequence, so it would be **granted**. But if it is asked *after* P1's grant above (Available = (2, 3, 0)), the new Available (2, 1, 0) cannot satisfy any Need, so it is **denied**. Safety is a property of the *current* state, so the same request can be safe or unsafe depending on history.

All of these tables were recomputed with `bca/tools/check_os.py`.
:::

**Drawbacks of the Banker's algorithm:** it needs advance maximum claims, the number of processes must be fixed, resources must not vanish, and the check costs O(m·n²) at every request. Hence it is taught more than it is used; real systems rely on prevention, detection and the ostrich.

## 4.6 Deadlock detection

If neither prevention nor avoidance is used, the OS periodically checks for deadlock.

**Single instance of each resource: wait-for graph.** Collapse the RAG by deleting resource nodes: Pᵢ → Pⱼ if Pᵢ waits for a resource held by Pⱼ. Deadlock exists iff this graph has a cycle. The check is O(n²) per run.

**Several instances: detection algorithm.** Same as the safety algorithm but using the current **Request** matrix instead of Need: a process whose Request ≤ Work is assumed to finish and release its allocation. Processes that cannot be marked finished at the end are deadlocked. (A process holding nothing is marked finished at the start.)

::: example Detection, with and without deadlock
Allocation (A B C): P0 = 0 1 0, P1 = 2 0 0, P2 = 3 0 3, P3 = 2 1 1, P4 = 0 0 2. Request: P0 = 0 0 0, P1 = 2 0 2, P2 = 0 0 0, P3 = 1 0 0, P4 = 0 0 2. Available = (0, 0, 0).

Work = (0, 0, 0). P0's request (0, 0, 0) fits: Work = (0, 1, 0). P2's request (0, 0, 0) fits: Work = (3, 1, 3). P1 requests (2, 0, 2) ≤ (3, 1, 3): Work = (5, 1, 3). P3 (1, 0, 0): Work = (7, 2, 4). P4 (0, 0, 2): Work = (7, 2, 6). Every process finished: **no deadlock**; order ⟨P0, P2, P1, P3, P4⟩.

Now suppose P2 makes one extra request, for one more C, so Request₂ = (0, 0, 1). Work = (0, 0, 0): only P0 can finish, giving Work = (0, 1, 0). Nothing else fits: P1 needs A and C, P2 needs a C, P3 needs an A, P4 needs C. **P1, P2, P3 and P4 are deadlocked.**
:::

**When to run it?** After every refused request (finds the deadlock early, but costly), every fixed interval, or when CPU utilisation falls below a threshold (a sign that processes are stuck).

## 4.7 Recovery from deadlock

**By terminating processes:**

- *Abort all* deadlocked processes: certain, but wasteful.
- *Abort one at a time* until the cycle disappears; the victim is chosen by priority, work done so far, resources held, resources still needed, and whether it is interactive or batch.

**By preempting resources:** take a resource away from one process and give it to another. Three issues: choose a **victim** (minimise cost), **rollback** the victim to a safe checkpoint and restart, and prevent **starvation** (do not always pick the same victim; include the number of rollbacks in the cost).

Another approach for processes that checkpoint: **rollback to the last checkpoint** before the resource was acquired.

## 4.8 Seeing the ideas: gridlock, graphs and the Banker

A deadlock is easy to recognise in real life. Four streets meet at a crossing, every driver is waiting for the car in front, and nobody can move. The photographs show such a gridlock and a railway signal gantry: the signals are the original semaphores, a lock on a section of track. Dijkstra named his synchronisation tool after them. The figures turn the pictures into resource-allocation graphs, the four conditions, safe and unsafe states and the Banker's trace.

```photogrid label="4.1" cols="3" ratio="1.0" caption="From the road to the resource graph. (a) A gridlock: each vehicle holds the space it occupies (hold) and waits for the space ahead (wait), nobody can be forced back (no preemption) and the waiting forms a circle. These are the four conditions for deadlock. (b) Railway signals guard a section of track; only one train may hold a section, exactly like a mutual-exclusion lock, and the word semaphore comes from this equipment. (c) The same situation as a resource-allocation graph: R1 is assigned to P1, P1 requests R2, R2 is assigned to P2 and P2 requests R1, so the cycle P1, R2, P2, R1 is a deadlock."
@ photo id="bca251/gridlock" cap="Gridlock: a circular wait"
fit 1.0
focus 0.5 0.5
call 0.5 0.5 0.04 0.9 "circular wait"
@ photo id="bca251/railsignal" cap="Railway semaphore signals"
fit 1.0
focus 0.5 0.3
call 0.5 0.3 0.04 0.9 "lock on a track"
@ svg cap="Resource-allocation graph with a cycle"
f = Fig(200, 190)
f.circle(45, 45, 21, fill=SAND, stroke=AMBER, label="P1", size=11)
f.circle(155, 135, 21, fill=SAND, stroke=AMBER, label="P2", size=11)
f.box(139, 29, 32, 32, "R2", fill=BLUE, stroke=NAVY, size=11, bold=True, r=0)
f.box(29, 119, 32, 32, "R1", fill=BLUE, stroke=NAVY, size=11, bold=True, r=0)
f.arrow([(45, 119), (45, 66)], color=TEAL, sw=1.8)
f.arrow([(66, 45), (139, 45)], color=RED, sw=1.8)
f.arrow([(155, 61), (155, 114)], color=TEAL, sw=1.8)
f.arrow([(134, 135), (61, 135)], color=RED, sw=1.8)
f.text(100, 100, "cycle =", size=10.5, color=RED, bold=True)
f.text(100, 116, "deadlock", size=10.5, color=RED, bold=True)
f.text(100, 178, "teal = assigned, red = requests", size=9.5, color=SLATE)
```

```svgfig label="4.1" caption="The four necessary conditions for deadlock and the way each prevention method breaks one of them. All four must hold at once; removing any one makes deadlock impossible. Mutual exclusion cannot usually be removed (a printer cannot be shared), so practical prevention attacks hold and wait, no preemption or circular wait."
f = Fig(580, 250)
rows = [("Mutual exclusion", "a resource is held by\none process only", "use spooling so that no\none holds the printer", TEAL),
        ("Hold and wait", "holds some resources and\nwaits for more", "request all at once, or\nrelease before asking", AMBER),
        ("No preemption", "resources cannot be taken\naway by force", "take back the resources\nof a waiting process", NAVY),
        ("Circular wait", "a ring of processes, each\nwaits for the next", "number the resources and\nrequest in increasing order", RED)]
f.text(80, 14, "condition", size=10.5, color=NAVY, bold=True)
f.text(265, 14, "meaning", size=10.5, color=NAVY, bold=True)
f.text(475, 14, "how prevention breaks it", size=10.5, color=NAVY, bold=True)
for i, (a, b, c, col) in enumerate(rows):
    y = 26 + i * 54
    f.box(8, y, 140, 46, a, fill=SOFT, stroke=col, size=10.5, bold=True)
    f.box(160, y, 210, 46, b, fill=SOFT, stroke="#cbd5e1", color=SLATE, size=9.5)
    f.box(382, y, 190, 46, c, fill=MINT, stroke=TEAL, size=9.5)
    f.arrow([(148, y + 23), (160, y + 23)], color=SLATE, sw=1.2)
    f.arrow([(370, y + 23), (382, y + 23)], color=SLATE, sw=1.2)
f.text(290, 244, "all four together = deadlock possible; break one = deadlock impossible", size=10, color=AMBER, bold=True)
```

```svgfig label="4.2" caption="Safe, unsafe and deadlocked states. Every deadlocked state is unsafe, but an unsafe state is not yet a deadlock: the processes might still release resources in time. A safe state guarantees that some order of the processes (a safe sequence) lets all of them finish. Deadlock avoidance, including the Banker's algorithm, grants a request only if the next state is still safe, so the system never enters the unsafe region."
f = Fig(580, 200)
f.box(10, 20, 200, 130, "SAFE\na safe sequence exists\nno deadlock possible", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(240, 20, 330, 130, "", fill=SAND, stroke=AMBER)
f.text(405, 38, "UNSAFE (no safe sequence)", size=11, color=AMBER, bold=True)
f.box(330, 62, 150, 70, "DEADLOCK\nprocesses stuck\nforever", fill=ROSE, stroke=RED, size=10.5, bold=True)
f.arrow([(210, 85), (240, 85)], color=SLATE, sw=1.6, label="a bad grant", lpos=(225, 74))
f.text(290, 176, "avoidance stays inside SAFE;  detection allows the other regions and repairs them", size=10, color=NAVY, bold=True)
```

```svgfig label="4.3" caption="Safety check of the Banker's algorithm for the five-process example (Available = 3 3 2 of totals 10, 5, 7). The vector Work grows as each process in the safe sequence finishes and returns its allocation: P1 needs 1 2 2 and fits in 3 3 2, giving 5 3 2; P3 gives 7 4 3; P4 gives 7 4 5; P0 gives 7 5 5; P2 gives 10 5 7, the full total. Because every process finished, the state is safe with the sequence P1, P3, P4, P0, P2."
f = Fig(580, 170)
steps = [("start", "3 3 2"), ("P1 done", "5 3 2"), ("P3 done", "7 4 3"), ("P4 done", "7 4 5"), ("P0 done", "7 5 5"), ("P2 done", "10 5 7")]
need = ["", "need 1 2 2", "need 0 1 1", "need 4 3 1", "need 7 4 3", "need 6 0 0"]
for i, ((a, w), n) in enumerate(zip(steps, need)):
    x = 8 + i * 95
    f.box(x, 40, 84, 50, "Work\n" + w, fill=MINT if i == 5 else BLUE, stroke=TEAL if i == 5 else NAVY, size=11, bold=True)
    f.text(x + 42, 28, a, size=10, color=NAVY, bold=True)
    f.text(x + 42, 106, n, size=9.5, color=SLATE)
    if i < 5:
        f.arrow([(x + 84, 65), (x + 95, 65)], color=SLATE, sw=1.5)
f.text(290, 140, "each step: need <= Work, then Work = Work + allocation", size=10.5, color=AMBER, bold=True)
f.text(290, 160, "safe sequence: P1, P3, P4, P0, P2", size=10.5, color=TEAL, bold=True)
```

```svgfig label="4.4" caption="Deadlock detection with a wait-for graph (single instance of each resource). An edge Pi to Pj means Pi waits for a resource held by Pj. Here P1 waits for P2, P2 waits for P3 and P3 waits for P1, a cycle, so P1, P2 and P3 are deadlocked. P4 waits for P1 but is not in the cycle; it is blocked, not deadlocked, and will run when the cycle is broken. Recovery kills one process of the cycle (for example P3) or preempts one of its resources."
f = Fig(580, 190)
f.circle(110, 40, 24, fill=ROSE, stroke=RED, label="P1", size=11)
f.circle(230, 40, 24, fill=ROSE, stroke=RED, label="P2", size=11)
f.circle(170, 140, 24, fill=ROSE, stroke=RED, label="P3", size=11)
f.circle(20, 140, 18, fill=SAND, stroke=AMBER, label="P4", size=10)
f.arrow([(134, 40), (206, 40)], color=RED, sw=1.8)
f.arrow([(222, 62), (186, 118)], color=RED, sw=1.8)
f.arrow([(152, 120), (118, 64)], color=RED, sw=1.8)
f.arrow([(36, 128), (92, 56)], color=AMBER, sw=1.6)
f.box(330, 25, 240, 130, "Algorithm\n1. build the wait-for graph\n2. search for a cycle (O(n^2))\n3. cycle found: deadlock\n4. kill or preempt to break it\nrun it often, or when CPU use drops", fill=SOFT, stroke=SLATE, size=9.5, bold=True)
```

### 4.8.1 Eight practical rules to avoid deadlock in programs

1. **Always lock in the same order.** If every thread takes lock A before lock B, a circle of waiting cannot form. For a money transfer in a banking program, lock the account with the smaller number first, whichever way the money flows. This one rule removes the circular-wait condition.
2. **Ask for everything at once.** A process that requests all its resources in a single step either gets them all or waits holding nothing. This breaks hold and wait. The price is that resources may stay idle for a while, so it suits short jobs.
3. **Use try-lock with a time-out.** If a lock cannot be obtained within a short time, release what you hold and try again later. This simulates preemption. A payment gateway such as Fonepay can use it to retry a failed database update instead of freezing.
4. **Keep critical sections short.** The less time a lock is held, the smaller the chance that another thread waits for it in a cycle. Do slow work such as network calls outside the lock. Short sections also improve speed.
5. **Avoid nested locks when you can.** Each extra lock held while taking another adds an edge to the possible wait-for graph. Where possible, copy the data you need and release the first lock. Simple designs have fewer deadlocks.
6. **Use higher-level tools.** Thread-safe queues, concurrent collections and message passing hide the locks and are tested by experts. A student project that uses a blocking queue is safer than one that uses five hand-written semaphores. This is the usual advice in the Java course.
7. **Let the database detect it.** Systems such as PostgreSQL and MySQL detect a deadlock between transactions, abort one and report an error. The application should catch the error and repeat the transaction. This is why exam-result and enrolment systems keep working under heavy load.
8. **Monitor and log.** Take thread dumps and watch for processes that are blocked for a long time. A wait-for graph built from the logs shows the cycle. Early detection turns a mystery freeze into a five-minute fix.

## Formula and fact sheet

- Four conditions: mutual exclusion, hold and wait, no preemption, circular wait.
- Need = Max − Allocation. Available = Total − ΣAllocation.
- Safe state ⇔ a safe sequence exists. Safe ⇒ no deadlock; unsafe ⇏ deadlock.
- Banker's request test: Request ≤ Need, Request ≤ Available, then pretend-allocate and run safety check.
- Detection uses Request (not Need). Single instance: wait-for graph cycle ⇔ deadlock.

## Chapter summary

- Deadlock needs mutual exclusion, hold-and-wait, no preemption and circular wait; breaking any one prevents it.
- RAGs show deadlocks as cycles (certain with single instances).
- Strategies: ostrich, prevention (ordering resources is most practical), avoidance (Banker's), detection with recovery.
- The Banker's algorithm keeps the system in safe states using maximum claims. Detection uses the same logic with current requests.
- Recovery means killing processes or preempting resources, while watching out for starvation.

## Practice

1. Define deadlock. List and explain the four necessary conditions.
2. Draw the RAG for two processes and two resources that is deadlocked, and give code for it.
3. Explain deadlock prevention by attacking each condition.
4. Differentiate safe, unsafe and deadlocked states.
5. Total resources (A, B, C) = (6, 4, 4). Allocation P0 = (1, 0, 1), P1 = (2, 1, 0), P2 = (1, 1, 1); Max P0 = (3, 2, 2), P1 = (3, 2, 1), P2 = (2, 2, 3). Is the state safe? Give a safe sequence.
6. In the Banker's example of this unit, can P3 ask for (0, 1, 1) in the original state? Show the check.
7. A system has 3 processes each needing 2 units of a resource with 4 units in total. Can it deadlock? What if there are only 3 units?
8. Describe detection with the wait-for graph and give two recovery methods.
9. Why is the ostrich algorithm used by most general-purpose operating systems?
10. A program locks mutexes in an order determined at run time. Propose a fix that makes deadlock impossible.

::: note Answers and worked solutions
**1.** Deadlock: a set of processes each waiting for an event only another in the set can cause. Conditions: *mutual exclusion* (resource not sharable); *hold and wait* (holds some, waits for more); *no preemption* (only the holder releases); *circular wait* (a cycle of waiting).
**2.** Edges R1 → P1, P1 → R2, R2 → P2, P2 → R1: a cycle with single-instance resources. Code: thread A: `lock(m1); lock(m2);`, thread B: `lock(m2); lock(m1);`.
**3.** Mutual exclusion: share or spool. Hold-and-wait: request everything at once. No preemption: release held resources if a request is refused. Circular wait: global resource ordering. (Details in 4.4.)
**4.** *Safe*: a safe sequence exists, deadlock cannot happen if we follow it. *Unsafe*: no such sequence; deadlock is possible, not certain. *Deadlocked*: the processes are already blocked in a cycle; a subset of unsafe states.
**5.** Allocated = (4, 2, 2), so Available = (6, 4, 4) − (4, 2, 2) = (2, 2, 2). Need: P0 = (2, 2, 1), P1 = (1, 1, 1), P2 = (1, 1, 2). P0: (2, 2, 1) ≤ (2, 2, 2): Work = (3, 2, 3). P1: (1, 1, 1) ≤ (3, 2, 3): Work = (5, 3, 3). P2: (1, 1, 2) ≤ (5, 3, 3): Work = (6, 4, 4). **Safe**, sequence ⟨P0, P1, P2⟩ (⟨P1, P0, P2⟩ also works).
**6.** Need₃ = (0, 1, 1), so Request = Need is allowed. Request ≤ Available (3, 3, 2) ✓. Pretend: Available = (3, 2, 1), Allocation₃ = (2, 2, 2), Need₃ = (0, 0, 0). P3 can finish at once (Need = 0): Work = (5, 4, 3). P1 (1, 2, 2) ≤ Work: (7, 4, 3). P0 (7, 4, 3) ≤ (7, 4, 3): (7, 5, 3). P2: (10, 5, 5). P4: (10, 5, 7). Safe, so **granted**.
**7.** With 4 units: worst case each process holds 1 (3 used) and one unit remains, which lets one process get 2 and finish: **no deadlock**. With 3 units: each holds 1, none free, each needs one more: **deadlock possible**. The rule: deadlock-free if units ≥ Σ(maxᵢ − 1) + 1 = 3 + 1 = 4.
**8.** Build the graph with an edge Pᵢ → Pⱼ when Pᵢ waits for Pⱼ; run cycle detection; any cycle is a deadlock. Recovery: abort one or all deadlocked processes; preempt a resource from a victim and roll the victim back.
**9.** Deadlocks are rare in practice, prevention would constrain programs and slow everything, and avoidance needs unknowable maximum claims. A manual restart once in a while is cheaper.
**10.** Assign each mutex a unique number (for example its address) and always acquire in ascending order, sorting the set before locking. Circular wait becomes impossible.
:::

## Model answers (5 and 10 marks)

**Q1. Define deadlock. State and explain the four necessary conditions. (5 marks)**

A **deadlock** is a situation in which a set of processes is blocked forever because each process holds a resource and waits for a resource held by another process of the set. For example, process P1 holds a printer and waits for a scanner, while P2 holds the scanner and waits for the printer; neither can proceed.

Deadlock can occur only if **all four** of the following conditions hold at the same time (Figure 4.1):

1. **Mutual exclusion:** at least one resource can be used by only one process at a time.
2. **Hold and wait:** a process holding at least one resource waits to acquire more resources held by others.
3. **No preemption:** a resource cannot be taken away by force; the holder must release it voluntarily.
4. **Circular wait:** there is a chain P1, P2, ..., Pn, P1 in which each process waits for a resource held by the next.

If any one condition is broken, deadlock cannot occur. Prevention methods work in this way: spooling removes mutual exclusion for printers, requesting all resources at once removes hold and wait, taking resources back removes no preemption, and ordering the resources removes circular wait. A gridlocked crossing (Plate 4.1) shows all four at once.

**Q2. What is a resource-allocation graph? How does it show a deadlock? (5 marks)**

A **resource-allocation graph (RAG)** is a directed graph that models the state of the resources. It has two kinds of vertices: processes (circles) and resource types (squares, with a dot for every instance). An edge from a process to a resource, P to R, is a **request edge**; an edge from a resource to a process, R to P, is an **assignment edge**.

**Reading the graph.**

- If the graph has **no cycle**, there is no deadlock.
- If it has a cycle and every resource has **one instance**, the cycle means deadlock.
- If it has a cycle but resources have **several instances**, deadlock is possible but not certain; another process outside the cycle may release an instance.

In the graph of Plate 4.1(c), R1 is assigned to P1, P1 requests R2, R2 is assigned to P2 and P2 requests R1. The cycle P1, R2, P2, R1, P1 with single-instance resources is a deadlock. A **wait-for graph** (Figure 4.4) is a simplified form that deletes the resource vertices, keeping only edges Pi to Pj, and is used for detection.

**Q3. Explain the methods of handling deadlock: ignoring, prevention, avoidance, detection and recovery. (10 marks)**

**Introduction.** A deadlock freezes a group of processes permanently. An operating system can handle the problem in four ways, depending on how often it occurs and how costly it is.

**1. Ignore it (ostrich algorithm).** Pretend that deadlocks never occur. UNIX and Windows do this for most resources because deadlocks are rare and prevention would cost more than the occasional reboot. The method is cheap but offers no protection.

**2. Prevention.** Design the system so that at least one of the four conditions can never hold. Request all resources at once (no hold and wait), allow preemption, or impose a total order on resource types (no circular wait). It is safe but lowers resource use and may cause starvation.

**3. Avoidance.** Let the OS examine every request and grant it only if the state remains **safe**, that is, a safe sequence exists. It needs advance knowledge of the maximum claim of each process. The Banker's algorithm is the standard method for multiple instances; the RAG algorithm with claim edges serves single instances.

**4. Detection.** Allow deadlock, then find it. The OS builds a wait-for graph (single instances) or runs a matrix algorithm (multiple instances) and looks for a cycle (Figure 4.4). It is run periodically or when CPU use drops.

**5. Recovery.** After detection, break the deadlock by **process termination** (kill all deadlocked processes, or one at a time until the cycle disappears, choosing the cheapest victim) or by **resource preemption** (take a resource from a victim, roll it back to a safe state and avoid starving the same victim).

| Method | Idea | Advantage | Disadvantage |
|---|---|---|---|
| Ignore | do nothing | no overhead | system may hang |
| Prevention | break a condition | deadlock impossible | low utilisation |
| Avoidance | stay in safe states | better utilisation | needs maximum claims |
| Detection and recovery | find and repair | no restriction on requests | recovery loses work |

**Conclusion.** General-purpose systems usually ignore deadlock or use detection; databases detect and abort a transaction; real-time and safety systems use prevention or avoidance because failure is not acceptable.

**Q4. Explain the Banker's algorithm. For the data below, find the Need matrix, test whether the state is safe and give a safe sequence. (10 marks)**

Total resources A, B, C = 10, 5, 7.

| Process | Allocation | Max |
|---|---|---|
| P0 | 0 1 0 | 7 5 3 |
| P1 | 2 0 0 | 3 2 2 |
| P2 | 3 0 2 | 9 0 2 |
| P3 | 2 1 1 | 2 2 2 |
| P4 | 0 0 2 | 4 3 3 |

**The algorithm.** The Banker's algorithm is a deadlock-avoidance method named after a bank that never lends so much money that it cannot satisfy all its customers. It keeps `Available` (free instances), `Max`, `Allocation` and `Need = Max - Allocation`. The **safety algorithm**: (1) set Work = Available and Finish[i] = false; (2) find a process with Finish[i] = false and Need[i] <= Work; (3) set Work = Work + Allocation[i] and Finish[i] = true, then repeat; (4) if all Finish are true, the state is safe. For a request, the OS checks Request <= Need and Request <= Available, pretends to grant it, and keeps the grant only if the new state is safe.

**Step 1: Need = Max - Allocation.**

| Process | Need (A B C) |
|---|---|
| P0 | 7 4 3 |
| P1 | 1 2 2 |
| P2 | 6 0 0 |
| P3 | 0 1 1 |
| P4 | 4 3 1 |

**Step 2: Available.** Allocation totals are (7, 2, 5), so Available = (10, 5, 7) - (7, 2, 5) = **(3, 3, 2)**.

**Step 3: Safety test (Figure 4.3).** Work = (3, 3, 2). P1 needs (1, 2, 2) and fits, so Work becomes (5, 3, 2). P3 needs (0, 1, 1), so Work = (7, 4, 3). P4 needs (4, 3, 1), so Work = (7, 4, 5). P0 needs (7, 4, 3), so Work = (7, 5, 5). P2 needs (6, 0, 0), so Work = (10, 5, 7), which equals the total, as it must.

**Result.** All processes can finish, so the state is **safe**, with the safe sequence **P1, P3, P4, P0, P2**. (The sequence is not unique; P1, P3, P0, P2, P4 also works.)

**Conclusion.** The Banker's algorithm avoids deadlock exactly, but needs maximum claims in advance, a fixed number of processes, and O(m x n^2) work for each request.

**Q5. Explain deadlock detection and recovery. (5 marks)**

**Detection.** When the system allows deadlock to occur, it must find it. With a **single instance** of each resource the OS maintains a wait-for graph with an edge Pi to Pj when Pi waits for a resource held by Pj, and searches it for a cycle. In Figure 4.4 the cycle P1, P2, P3 shows that these three are deadlocked, while P4 is only blocked behind P1. With **multiple instances** the OS uses a matrix algorithm similar to the Banker's safety test, with Allocation and current Request matrices; processes that cannot finish are deadlocked. Detection is run at fixed intervals or when CPU utilisation falls.

**Recovery.**

1. **Terminate all** deadlocked processes: simple but expensive, as all work is lost.
2. **Terminate one at a time** until the cycle is broken, choosing the victim by priority, work done, resources held and the cost of restarting.
3. **Preempt resources:** take a resource from a victim, roll the victim back to a safe state, and restart it later. To avoid starvation, count how often a process has been chosen as victim.

For example, killing P3 in Figure 4.4 removes the cycle, and P1, P2 and P4 can continue. Databases do the same by aborting one transaction of a deadlock and asking the application to retry it.
