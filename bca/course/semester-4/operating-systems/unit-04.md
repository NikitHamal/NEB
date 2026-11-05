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
