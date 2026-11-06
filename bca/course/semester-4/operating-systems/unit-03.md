---
subject: Operating Systems
grade: BCA Semester 4
unit: 3
title: Process Management
hours: 15
area: BCA 251 · Operating Systems · Unit 3
---

This is the heart of the course and the biggest share of exam marks. A program on disk is just a file; the OS turns it into a living **process**, shares the CPU among processes, lets them cooperate without corrupting shared data, and decides who runs next. The unit has four parts: process concepts, threads, inter-process communication and synchronization, and scheduling.

::: key What this unit gives you
- Process model, states, the process control block, operations on processes, system calls, with working C programs.
- Threads and multithreading models.
- Race conditions, critical regions, mutual exclusion (Peterson, TSL, semaphores, monitors), classical IPC problems, serializability.
- CPU scheduling (FCFS, SJF, SRTF, priority, round robin, multilevel queues and more) with verified numerical examples.
:::

## 3.1 Process concepts

### Definition and the process model

A **program** is passive: instructions stored on disk. A **process** is a program in execution: the code, the current values of the program counter and registers, a stack (parameters, return addresses, locals), a data section (globals) and a heap (dynamic memory). Two processes can run the same program (two terminal windows) and are still two processes with separate data.

In the **process model**, all runnable software is organised into sequential processes. Conceptually each has its own virtual CPU; in reality the real CPU switches among them (multiprogramming). Because the switching is fast, we may think of them as running in parallel.

### Process states and transitions

| State | Meaning |
|---|---|
| **New** | being created |
| **Ready** | in memory, waiting for the CPU |
| **Running** | instructions are executing on the CPU |
| **Waiting (blocked)** | waiting for an event (I/O completion, a signal) |
| **Terminated** | finished; resources being reclaimed |

The legal transitions:

| From → To | Cause |
|---|---|
| New → Ready | the OS admits the process |
| Ready → Running | the **scheduler dispatches** it |
| Running → Ready | its time slice expires (**preemption**) or a higher-priority process arrives |
| Running → Waiting | it requests I/O or waits for an event |
| Waiting → Ready | the I/O or event completes |
| Running → Terminated | it calls `exit` or is killed |

Note what is *not* possible: a waiting process never moves straight to running, it must pass through ready, and a ready process cannot block (only a running one can ask for I/O).

### The process control block (PCB)

The OS keeps one **PCB** (task control block) per process. It holds everything needed to stop the process and resume it later:

- process ID, parent ID, state;
- program counter and CPU registers (saved at a context switch);
- scheduling information: priority, queue pointers, CPU time used;
- memory-management information: base/limit registers or page-table pointer;
- accounting information: CPU time, time limits;
- I/O status: open files, devices allocated.

A **context switch** saves the state of the running process in its PCB and loads the state of the next. It is pure overhead, no useful work, typically a few microseconds, and it also disturbs the CPU caches.

### Operations on processes

**Creation.** A process creates another through a system call (UNIX `fork`, Windows `CreateProcess`). The creator is the **parent**, the new one the **child**, so processes form a **hierarchy** (a tree: `init`/`systemd` is the root on Linux). In Windows there is no hierarchy once the child is created; the parent holds a handle which can be passed on. Reasons for creation: system initialisation, a user command, a batch job, a running process asking for helpers.

**Termination.** A process ends by normal exit (voluntary), error exit (voluntary, e.g. file not found), fatal error (involuntary, e.g. division by zero or illegal memory access) or being killed by another process. A parent may terminate children (cascading termination) if it exits first on some systems; on UNIX orphans are adopted by `init`.

**Implementation.** The OS keeps a **process table** (an array or list of PCBs). `fork` makes a new PCB, copies the parent's address space (nowadays *copy-on-write*), and returns twice: 0 in the child and the child's PID in the parent.

::: example fork and wait in C
The program forks a child. The child's copy of `x` is separate from the parent's: changing it in the child does not affect the parent.

```c
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    int x = 10;
    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return 1; }
    if (pid == 0) {              /* child */
        x += 5;
        printf("child : x = %d\n", x);
        return 7;
    }
    int status;
    waitpid(pid, &status, 0);    /* parent waits for the child */
    printf("parent: x = %d, child exited with %d\n", x, WEXITSTATUS(status));
    return 0;
}
```
```output
child : x = 15
parent: x = 10, child exited with 7
```
:::

Both copies resume after `fork`; the `if` separates their paths. Without the `waitpid`, the output order would depend on the scheduler, and a child that ends before the parent collects its status becomes a **zombie** (a PCB kept only so the parent can read the exit code).

### Cooperating processes and communication

An **independent** process cannot affect or be affected by others. A **cooperating** process can; reasons are information sharing, computation speed-up on multiple CPUs, modularity and convenience. Cooperation needs inter-process communication, either **shared memory** (fast, but needs synchronization) or **message passing** (slower, easier, works across machines). A **pipe** is the simplest message channel on UNIX:

```c
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>

int main(void) {
    int fd[2];
    char buf[64];
    if (pipe(fd) == -1) return 1;
    if (fork() == 0) {                       /* child: reader */
        close(fd[1]);
        ssize_t n = read(fd[0], buf, sizeof buf - 1);
        buf[n] = '\0';
        printf("child read: %s\n", buf);
        return 0;
    }
    close(fd[0]);                            /* parent: writer */
    const char *msg = "namaste from parent";
    if (write(fd[1], msg, strlen(msg)) < 0) return 1;
    close(fd[1]);
    wait(NULL);
    printf("parent done\n");
    return 0;
}
```
```output
child read: namaste from parent
parent done
```

### System calls for processes, files and directories

| Area | POSIX call | Purpose |
|---|---|---|
| Process | `fork()`, `execve()`, `waitpid()`, `exit()`, `kill()` | create, replace image, wait, end, signal |
| File | `open()`, `close()`, `read()`, `write()`, `lseek()`, `stat()` | file I/O and attributes |
| Directory | `mkdir()`, `rmdir()`, `link()`, `unlink()`, `mount()` | namespace changes |
| Protection | `chmod()`, `chown()`, `umask()` | permissions |

`fork` + `execve` is how a shell starts a program: the child replaces its image with the new program while the parent waits.

## 3.2 Threads

A **thread** is a lightweight unit of CPU execution inside a process. A **single-threaded** process has one thread of control. A **multithreaded** process has several that **share** the code, data, heap and open files but each has its **own** program counter, registers and stack.

| Item | Per process | Per thread |
|---|---|---|
| Address space, global variables, open files, signal handlers | ✔ | |
| Program counter, registers, stack, state | | ✔ |

**Benefits of multithreading:**

- **Responsiveness**: a browser keeps drawing while another thread downloads.
- **Resource sharing**: threads share memory by default, with no IPC needed.
- **Economy**: creating a thread and switching between threads is much cheaper than for processes.
- **Scalability**: threads run truly in parallel on different cores.

The price: shared data means every thread can corrupt it, which brings the synchronization problems of Section 3.3.

### Multithreading models

User-level threads are managed by a library, the kernel is unaware of them; kernel-level threads are managed by the OS. Mapping user threads onto kernel threads gives three models:

| Model | Mapping | Pros | Cons |
|---|---|---|---|
| **Many-to-one** | many user threads → one kernel thread | cheap, no kernel involvement | one blocking call blocks all; no parallelism |
| **One-to-one** | each user thread → its own kernel thread | true parallelism, a blocking call blocks only one | creating many threads is costly (Linux, Windows use this) |
| **Many-to-many** | *m* user threads → *n* ≤ *m* kernel threads | combines both | complex to implement |

### Threads in C (POSIX threads)

This program creates four threads that each square a number and store the result in a different array slot, so no synchronization is needed:

```c
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <pthread.h>

static long result[4];

static void *square(void *arg) {
    long n = (long)arg;
    result[n] = n * n;
    return NULL;
}

int main(void) {
    pthread_t t[4];
    for (long i = 0; i < 4; i++) pthread_create(&t[i], NULL, square, (void *)i);
    for (int i = 0; i < 4; i++) pthread_join(t[i], NULL);
    for (int i = 0; i < 4; i++) printf("%d squared = %ld\n", i, result[i]);
    return 0;
}
```
```output
0 squared = 0
1 squared = 1
2 squared = 4
3 squared = 9
```

## 3.3 Inter-process communication and synchronization

### Race condition

When two or more processes read and write shared data and the result depends on the *exact order* in which their instructions interleave, we have a **race condition**. `counter++` is not one machine step; it is *load, add, store*. Two threads can both load 5, both add 1, and both store 6, losing one increment.

The program below runs two threads that each increment a shared counter one million times, first with no protection and then with a mutex. The first result is wrong and changes from run to run (that is the point); the second is always 2,000,000.

```c
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <pthread.h>

static volatile long unsafe = 0;
static long safe = 0;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

static void *work(void *arg) {
    (void)arg;
    for (int i = 0; i < 1000000; i++) {
        unsafe++;                       /* race: load, add, store */
        pthread_mutex_lock(&lock);
        safe++;                         /* protected */
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}

int main(void) {
    pthread_t a, b;
    pthread_create(&a, NULL, work, NULL);
    pthread_create(&b, NULL, work, NULL);
    pthread_join(a, NULL);
    pthread_join(b, NULL);
    printf("no lock  : %ld (expected 2000000)\n", unsafe);
    printf("with lock: %ld\n", safe);
    return 0;
}
```
```output
no lock  : 1967268 (expected 2000000)
with lock: 2000000
```

### Critical regions and the three requirements

The part of a program that accesses shared data is its **critical section (critical region)**. A correct solution to the critical-section problem must satisfy:

1. **Mutual exclusion**: no two processes are inside their critical sections at the same time.
2. **Progress**: if no process is in its critical section and some want to enter, only those wanting to enter decide who goes next, and the decision cannot be postponed forever.
3. **Bounded waiting**: there is a limit on how many times others can enter ahead of a process that has asked.

No assumptions may be made about the relative speeds or the number of CPUs.

### Proposals for achieving mutual exclusion

**Disabling interrupts.** Each process disables interrupts on entry and re-enables them on exit, so the CPU cannot be taken away. *Useful inside the kernel* for very short sections, but dangerous for users: a program that forgets to re-enable stops the system, and it does not work on multiprocessors (other CPUs still run).

**Lock variable.** A shared variable `lock` (0 = free). A process tests it and, if 0, sets it to 1 and enters. **Flawed:** two processes can both read 0 before either writes 1, so both enter; the race has only moved to the lock variable.

**Strict alternation.** A shared `turn` says whose turn it is: process 0 enters when `turn == 0` and sets `turn = 1` on exit, and vice versa. Mutual exclusion holds but it uses **busy waiting** (spin lock) and violates *progress*: a slow process can block a fast one that wants to enter twice in a row.

**Peterson's solution (software, two processes).** Combines `turn` and a `flag[]` array. Process *i* (other is *j*):

```text
flag[i] = true;          // I want to enter
turn = j;                // but you go first if you also want
while (flag[j] && turn == j)
    ;                    // busy wait
/* critical section */
flag[i] = false;         // leave
```

If both want to enter, both set `turn`; the one that wrote last loses and waits, so exactly one enters. It satisfies mutual exclusion, progress and bounded waiting, but on modern CPUs, which reorder memory accesses, it needs memory barriers to work.

**The TSL (test and set lock) instruction.** Hardware helps: `TSL R, LOCK` copies the old value of `LOCK` into register R and sets `LOCK` to 1 in **one indivisible step** (the bus is locked). A process enters when it reads 0:

```text
enter_region:  TSL REGISTER, LOCK    ; atomic read-and-set
               CMP REGISTER, #0
               JNE enter_region      ; was 1: someone is inside, try again
               RET
leave_region:  MOVE LOCK, #0
               RET
```

It works for any number of processes and CPUs, but it still burns CPU while waiting (a **spin lock**), and a high-priority spinner can starve the low-priority lock-holder (**priority inversion**).

### Sleep and wakeup; the producer-consumer problem

Busy waiting wastes CPU. The primitives `sleep` (block until woken) and `wakeup` (move to ready) let a process block. In the **producer-consumer (bounded buffer)** problem, a producer puts items into a buffer of *N* slots and a consumer takes them out. The producer must sleep when the buffer is full, the consumer when it is empty. With only a shared `count`, a **lost wakeup** can occur: the consumer reads `count == 0` and is about to sleep, the producer inserts an item and sends a wakeup before the consumer is actually asleep, the wakeup is lost, and both sleep forever. This motivated semaphores.

### Semaphores

Dijkstra (1965): a **semaphore** is an integer variable accessed only through two atomic operations.

```text
down(S) / wait(S) / P(S):  if S > 0 then S = S - 1 else block the caller
up(S)   / signal(S) / V(S): if some process is blocked on S wake one, else S = S + 1
```

A **binary semaphore** (0 or 1) gives mutual exclusion; a **counting semaphore** counts units of a resource. In the bounded buffer, three semaphores solve the problem: `mutex = 1` (exclusive access), `empty = N` (free slots), `full = 0` (filled slots). The producer does `down(empty); down(mutex); insert; up(mutex); up(full)`; the consumer does `down(full); down(mutex); remove; up(mutex); up(empty)`. **Order matters**: swapping `down(empty)` and `down(mutex)` in the producer can deadlock (a producer holding the mutex sleeps on a full buffer, and the consumer cannot get the mutex to empty it).

Below is a working version with POSIX semaphores. The producer makes 1 to 20; the consumer sums them; the buffer has five slots:

```c
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>

#define N 5
static int buf[N], in = 0, out = 0;
static sem_t empty, full;
static pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;

static void *producer(void *arg) {
    (void)arg;
    for (int i = 1; i <= 20; i++) {
        sem_wait(&empty);
        pthread_mutex_lock(&mtx);
        buf[in] = i; in = (in + 1) % N;
        pthread_mutex_unlock(&mtx);
        sem_post(&full);
    }
    return NULL;
}

static void *consumer(void *arg) {
    (void)arg;
    int sum = 0;
    for (int k = 0; k < 20; k++) {
        sem_wait(&full);
        pthread_mutex_lock(&mtx);
        sum += buf[out]; out = (out + 1) % N;
        pthread_mutex_unlock(&mtx);
        sem_post(&empty);
    }
    printf("consumed 20 items, sum = %d\n", sum);
    return NULL;
}

int main(void) {
    pthread_t p, c;
    sem_init(&empty, 0, N);
    sem_init(&full, 0, 0);
    pthread_create(&p, NULL, producer, NULL);
    pthread_create(&c, NULL, consumer, NULL);
    pthread_join(p, NULL);
    pthread_join(c, NULL);
    return 0;
}
```
```output
consumed 20 items, sum = 210
```

### Mutexes, monitors and message passing

A **mutex** is a simplified binary semaphore with two states (locked, unlocked) used only for mutual exclusion; the thread that locks it must unlock it. A **monitor** (Hoare, Brinch Hansen) is a language construct, a module in which *only one process at a time can be active*; the compiler adds the locking. Condition variables with `wait` and `signal` let a process sleep inside a monitor without blocking others (Java's `synchronized`, `wait()` and `notify()` follow this idea). **Message passing** uses `send(dest, msg)` and `receive(src, msg)`; it needs no shared memory, so it works across machines, and a blocking `receive` provides synchronization. The bounded buffer can be solved with *N* messages circulating between producer and consumer.

### Classical IPC problems

**Dining philosophers.** Five philosophers sit at a round table with one fork between each pair; each needs *both* adjacent forks to eat. If all pick up their left fork at once, nobody can get a right fork: **deadlock**. Remedies: allow at most four to sit; pick both forks only if both are free (inside a critical section); or break symmetry by an **ordering rule**: number the forks and always take the lower-numbered first (so one philosopher takes right-then-left). The program below uses the ordering rule, and every philosopher eats three times:

```c
#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <pthread.h>

#define P 5
static pthread_mutex_t fork_m[P];
static int meals[P];

static void *philosopher(void *arg) {
    int id = (int)(long)arg;
    int a = id, b = (id + 1) % P;
    if (a > b) { int t = a; a = b; b = t; }     /* lower fork first */
    for (int k = 0; k < 3; k++) {
        pthread_mutex_lock(&fork_m[a]);
        pthread_mutex_lock(&fork_m[b]);
        meals[id]++;                            /* eat */
        pthread_mutex_unlock(&fork_m[b]);
        pthread_mutex_unlock(&fork_m[a]);
    }
    return NULL;
}

int main(void) {
    pthread_t t[P];
    for (int i = 0; i < P; i++) pthread_mutex_init(&fork_m[i], NULL);
    for (long i = 0; i < P; i++) pthread_create(&t[i], NULL, philosopher, (void *)i);
    for (int i = 0; i < P; i++) pthread_join(t[i], NULL);
    for (int i = 0; i < P; i++) printf("philosopher %d ate %d times\n", i, meals[i]);
    return 0;
}
```
```output
philosopher 0 ate 3 times
philosopher 1 ate 3 times
philosopher 2 ate 3 times
philosopher 3 ate 3 times
philosopher 4 ate 3 times
```

**Readers-writers.** Many readers may read a database at once, but a writer needs exclusive access. *First* readers-writers (readers' priority): the first reader locks out writers, the last reader lets them in again, using a `readcount` protected by a mutex and a semaphore `db`. It can starve writers; the second version gives writers priority and can starve readers.

**Sleeping barber.** A barber shop has one barber, one chair and *n* waiting chairs. With no customers the barber sleeps. A customer who arrives finding the barber asleep wakes him; if the barber is busy the customer sits in a waiting chair, or leaves if all are full. Solved with three semaphores: `customers` (waiting customers, initially 0), `barbers` (idle barbers, initially 0) and `mutex` guarding a counter of waiting customers. It demonstrates avoiding both race conditions and lost wakeups.

### Serializability, locking and timestamp protocols

Synchronization also appears where several **transactions** access shared data (databases, Unit 9 of the DBMS book). A schedule is **serializable** if its result equals that of some serial order of the same transactions. Two operations **conflict** if they belong to different transactions, access the same item and at least one is a write. Draw an edge *Ti → Tj* for each conflict where Ti's operation comes first; the schedule is **conflict-serializable** iff this *precedence graph* has no cycle.

::: example Lost update is non-serializable
Schedule: R1(A), R2(A), W1(A), W2(A). Conflicts: R1(A) before W2(A) gives T1 → T2; R2(A) before W1(A) gives T2 → T1. The graph has a cycle, so the schedule is not serializable and indeed T1's update is overwritten (lost update). The schedule R1(A), W1(A), R2(A), W2(A) has only T1 → T2 and is equivalent to the serial order T1, T2.
:::

**Locking protocols.** Transactions take shared (S) locks to read and exclusive (X) locks to write. In **two-phase locking (2PL)**, each transaction has a *growing* phase (acquire locks only) followed by a *shrinking* phase (release only); 2PL guarantees conflict serializability but not freedom from deadlock. *Strict 2PL* holds exclusive locks to commit time, which also prevents cascading aborts.

**Timestamp protocols.** Each transaction *T* gets a unique timestamp TS(T) when it starts; each item *Q* keeps R-ts(Q) and W-ts(Q), the largest timestamps of readers and writers. Rules:

- Read(Q) by T: if TS(T) < W-ts(Q), T would read an already overwritten value, so **roll back** T; otherwise execute and set R-ts(Q) = max(R-ts(Q), TS(T)).
- Write(Q) by T: if TS(T) < R-ts(Q) or TS(T) < W-ts(Q), **roll back** T; otherwise execute and set W-ts(Q) = TS(T).

The order of timestamps becomes the equivalent serial order. There are no locks and so no deadlocks, but rolled-back transactions restart with a new timestamp.

## 3.4 Process scheduling

### Basic concepts and types

When more than one process is ready, the **scheduler** chooses. The **dispatcher** performs the context switch and jumps to the chosen process (*dispatch latency* = its time). CPU bursts alternate with I/O bursts; an **I/O-bound** process has many short CPU bursts, a **CPU-bound** one a few long bursts.

- **Non-preemptive**: once given the CPU, a process keeps it until it blocks or exits. Simple; poor response.
- **Preemptive**: the OS can take the CPU back (timer interrupt, higher-priority arrival). Better response; needs care over shared kernel data.
- By environment: **batch** (throughput, no users waiting, long quanta fine), **interactive** (response time, preemption essential), **real-time** (deadlines).

### Scheduling criteria

| Criterion | Meaning | Goal |
|---|---|---|
| CPU utilisation | fraction of time CPU is busy | maximise |
| Throughput | processes completed per unit time | maximise |
| Turnaround time (TAT) | completion time − arrival time | minimise |
| Waiting time (WT) | TAT − burst time (time spent in the ready queue) | minimise |
| Response time | arrival → first response | minimise |

Formulas: **TAT = CT − AT**, **WT = TAT − BT**, where CT is completion time, AT arrival time and BT burst time.

### First-come first-served (FCFS)

Non-preemptive; the ready queue is a FIFO. Easy but the **convoy effect**: short processes wait behind a long one. Use this process set for the next four algorithms (arrival, burst): P1 (0, 8), P2 (1, 4), P3 (2, 9), P4 (3, 5).

Gantt chart: P1[0–8] P2[8–12] P3[12–21] P4[21–26].

| P | AT | BT | CT | TAT | WT |
|---|---|---|---|---|---|
| P1 | 0 | 8 | 8 | 8 | 0 |
| P2 | 1 | 4 | 12 | 11 | 7 |
| P3 | 2 | 9 | 21 | 19 | 10 |
| P4 | 3 | 5 | 26 | 23 | 18 |

Average TAT = 15.25, **average WT = 8.75**.

### Shortest job first (SJF, shortest process next)

Choose the ready process with the smallest next CPU burst. It is **provably optimal** for minimum average waiting time among non-preemptive algorithms but needs the future burst length, which is *predicted* by exponential averaging: τₙ₊₁ = α·tₙ + (1 − α)·τₙ, where tₙ is the last measured burst and τₙ the last prediction. With α = ½ and τ₀ = 10, measured bursts 6, 4, 6, 4, 13, 13, 13 give predictions 8, 6, 6, 5, 9, 11, 12. SJF can **starve** long processes.

Non-preemptive SJF on the set above: Gantt P1[0–8] P2[8–12] P4[12–17] P3[17–26]. At time 8, P2, P3, P4 are ready with bursts 4, 9, 5, so P2 goes first, then P4, then P3.

| P | AT | BT | CT | TAT | WT |
|---|---|---|---|---|---|
| P1 | 0 | 8 | 8 | 8 | 0 |
| P2 | 1 | 4 | 12 | 11 | 7 |
| P3 | 2 | 9 | 26 | 24 | 15 |
| P4 | 3 | 5 | 17 | 14 | 9 |

Average TAT = 14.25, **average WT = 7.75**.

### Shortest remaining time next (SRTF)

The preemptive version of SJF: when a process arrives with a burst shorter than the *remaining* time of the running one, it preempts. Gantt: P1[0–1] P2[1–5] P4[5–10] P1[10–17] P3[17–26]. P1 runs one unit, P2 arrives with burst 4 < 7 remaining, and preempts; P3 (9) never beats the shortest, and P4 (5) is shorter than P1's remaining 7 at time 5.

| P | AT | BT | CT | TAT | WT |
|---|---|---|---|---|---|
| P1 | 0 | 8 | 17 | 17 | 9 |
| P2 | 1 | 4 | 5 | 4 | 0 |
| P3 | 2 | 9 | 26 | 24 | 15 |
| P4 | 3 | 5 | 10 | 7 | 2 |

Average TAT = 13.00, **average WT = 6.50**, the best of the three on this set, as theory predicts.

### Priority scheduling

Each process has a priority; the CPU goes to the highest (here, a smaller number means higher priority). It may be preemptive or not. Danger: **starvation** of low-priority processes; cure: **aging**, which raises the priority of a process the longer it waits. Example, all arriving at time 0 (burst, priority): P1 (10, 3), P2 (1, 1), P3 (2, 4), P4 (1, 5), P5 (5, 2). Order by priority: P2, P5, P1, P3, P4.

| P | AT | BT | CT | TAT | WT |
|---|---|---|---|---|---|
| P1 | 0 | 10 | 16 | 16 | 6 |
| P2 | 0 | 1 | 1 | 1 | 0 |
| P3 | 0 | 2 | 18 | 18 | 16 |
| P4 | 0 | 1 | 19 | 19 | 18 |
| P5 | 0 | 5 | 6 | 6 | 1 |

Average TAT = 12.00, **average WT = 8.20**.

### Round robin (RR)

Designed for time-sharing: each process gets a **time quantum** *q*, then goes to the end of the ready queue. If *n* processes are ready, no process waits more than (n − 1)·q before getting the CPU. The choice of *q* matters: if *q* is very large RR becomes FCFS; if *q* is very small, context-switch overhead dominates. With *q* = 4 ms and a 1 ms switch, 1/(4+1) = **20 %** of the CPU is wasted. A common rule of thumb is that about 80 % of bursts should be shorter than *q*.

Example with the classic bursts 24, 3, 3 (all arrive at 0), *q* = 4. Gantt: P1[0–4] P2[4–7] P3[7–10] then P1 runs alone from 10 to 30.

| P | AT | BT | CT | TAT | WT |
|---|---|---|---|---|---|
| P1 | 0 | 24 | 30 | 30 | 6 |
| P2 | 0 | 3 | 7 | 7 | 4 |
| P3 | 0 | 3 | 10 | 10 | 7 |

**Average WT = 5.67**, whereas FCFS on the same set (P1, P2, P3) gives (0 + 24 + 27)/3 = **17.00**: RR rescues the short jobs from the convoy. On the first set with *q* = 3: Gantt P1[0–3] P2[3–6] P3[6–9] P4[9–12] P1[12–15] P2[15–16] P3[16–19] P4[19–21] P1[21–23] P3[23–26], giving WTs 15, 11, 15, 13 and **average WT = 13.50**, much worse than SJF: RR trades turnaround for fairness and quick first response.

::: caution A tie-breaking rule you must state
When a process arrives at the same instant another's quantum expires, conventions differ about which enters the ready queue first. This book puts the *new arrival* in the queue before the pre-empted process. State your convention in the exam, since different books give different (equally valid) tables.
:::

### Other algorithms

| Algorithm | Idea |
|---|---|
| **Highest response ratio next (HRN / HRRN)** | non-preemptive; pick the largest (waiting + burst) / burst, which favours short jobs yet ages long ones. On the first set: at time 8, ratios P2 = (7+4)/4 = 2.75, P3 = (6+9)/9 = 1.67, P4 = (5+5)/5 = 2.0, so P2; at time 12, P3 = 2.11 and P4 = (9+5)/5 = 2.80, so P4; then P3. Same order as SJF here. |
| **Multiple (multilevel) queues** | ready queue split into foreground (RR) and background (FCFS) queues with fixed priority between queues or time slices |
| **Multilevel feedback queue (MLFQ)** | processes move between queues: a process that uses its whole quantum drops to a lower queue; one that waits too long moves up (aging). Favours I/O-bound and interactive jobs without knowing burst lengths in advance |
| **Guaranteed scheduling** | promise each of *n* users 1/n of CPU time; run the process with the lowest ratio of actual time to entitled time |
| **Lottery scheduling** | processes hold tickets; each quantum a random ticket is drawn. A process with 60 of 100 tickets gets about 60 % of the CPU in the long run |
| **Fair-share** | share is divided per *user*, not per process, so a user running many processes cannot starve another |
| **Real-time** | **rate-monotonic (RMS)**: static priority, shorter period = higher; schedulable if Σ Cᵢ/Tᵢ ≤ n(2^(1/n) − 1) (about 0.78 for n = 3, tending to ln 2 ≈ 0.693). **Earliest-deadline-first (EDF)**: dynamic; schedulable iff Σ Cᵢ/Tᵢ ≤ 1 |

::: example Real-time check
Three periodic tasks (run time C, period T): (1, 4), (2, 6), (1, 8). Utilisation = 1/4 + 2/6 + 1/8 = 0.25 + 0.333 + 0.125 = **0.708**. The RMS bound for n = 3 is 3(2^(1/3) − 1) = **0.7798**, and 0.708 ≤ 0.7798, so RMS guarantees all deadlines; EDF would as well since 0.708 ≤ 1.
:::

## 3.5 Seeing the ideas: states, races, semaphores and schedules

Process management is the heart of an operating system and the most examined unit. The plate links three everyday pictures to the three big ideas of the unit: a ticket queue is a ready queue, five diners and five forks are a synchronisation puzzle, and Edsger Dijkstra gave us the semaphore. The figures then draw the process states, a race condition, a semaphore-protected buffer, the thread models and four schedules whose averages are computed from a single data set.

```photogrid label="3.1" cols="3" ratio="1.1" caption="Three pictures for three ideas. (a) A queue at a ticket window is the ready queue: the process at the front gets the CPU next, and the scheduling algorithm decides who stands at the front. (b) The dining philosophers: five philosophers share five forks, and each needs two. If all pick up their left fork together, nobody can eat, which is a deadlock. (c) Edsger Dijkstra, who invented the semaphore (P and V operations) and posed the dining philosophers problem in 1965."
@ photo id="bca201/queue" cap="Ticket queue = ready queue"
fit 1.1
focus 0.5 0.5
call 0.3 0.5 0.04 0.9 "front = next to run"
@ photo id="bca251/philosophers" cap="Dining philosophers"
fit 1.1
focus 0.5 0.5
call 0.5 0.5 0.04 0.9 "5 forks, 5 diners"
@ photo id="bca201/dijkstra" cap="Edsger W. Dijkstra"
fit 1.1
focus 0.5 0.3
call 0.5 0.5 0.04 0.9 "inventor of P and V"
```

```svgfig label="3.1" caption="The five-state process model. A new process is admitted to the ready queue. The dispatcher moves one ready process to running. A running process returns to ready when its time slice ends (timer interrupt), moves to waiting when it requests I/O or an event, and to terminated when it finishes. When the I/O completes, the process moves from waiting back to ready, never directly to running."
f = Fig(580, 230)
f.circle(60, 100, 36, fill=SOFT, stroke=SLATE, label="New", size=10.5)
f.circle(200, 100, 38, fill=SAND, stroke=AMBER, label="Ready", size=10.5)
f.circle(380, 100, 38, fill=MINT, stroke=TEAL, label="Running", size=10.5)
f.circle(520, 100, 38, fill=ROSE, stroke=RED, label="Done", size=10.5)
f.circle(290, 200, 30, fill=BLUE, stroke=NAVY, label="Waiting", size=10)
f.arrow([(96, 100), (162, 100)], color=SLATE, sw=1.6, label="admit", lpos=(129, 90))
f.arrow([(238, 88), (342, 88)], color=TEAL, sw=1.6, label="dispatch", lpos=(290, 78))
f.arrow([(342, 112), (238, 112)], color=AMBER, sw=1.6, label="timeout", lpos=(290, 126))
f.arrow([(418, 100), (482, 100)], color=RED, sw=1.6, label="exit", lpos=(450, 90))
f.arrow([(360, 134), (310, 176)], color=NAVY, sw=1.6, label="I/O request", lpos=(372, 168))
f.arrow([(268, 178), (218, 134)], color=NAVY, sw=1.6, label="I/O done", lpos=(206, 168))
f.text(290, 18, "only the dispatcher can move a process from Ready to Running", size=10, color=AMBER, bold=True)
```

```svgfig label="3.2" caption="A race condition on a shared counter. Two threads share count = 5. Thread 1 executes count++ and Thread 2 executes count--, so the correct final value is 5. Each statement is really three machine steps (load, change, store). In the interleaving shown, both threads load 5, Thread 1 stores 6 and then Thread 2 stores 4, so the update of Thread 1 is lost and the result is 4. Run in a different order the result could be 5 or 6, which is why the outcome cannot be trusted."
f = Fig(580, 250)
f.text(120, 14, "Thread 1: count++", size=10.5, color=NAVY, bold=True)
f.text(290, 14, "Thread 2: count--", size=10.5, color=RED, bold=True)
f.text(480, 14, "shared count", size=10.5, color=SLATE, bold=True)
rows = [("1  r1 = count (5)", "", "5"), ("", "2  r2 = count (5)", "5"), ("3  r1 = r1 + 1 (6)", "", "5"), ("", "4  r2 = r2 - 1 (4)", "5"), ("5  count = r1", "", "6"), ("", "6  count = r2", "4")]
for i, (a, b, c) in enumerate(rows):
    y = 28 + i * 30
    f.box(10, y, 220, 26, a, fill=BLUE if a else SOFT, stroke=NAVY if a else "#cbd5e1", size=10, bold=bool(a))
    f.box(235, y, 215, 26, b, fill=ROSE if b else SOFT, stroke=RED if b else "#cbd5e1", size=10, bold=bool(b))
    f.box(480, y, 60, 26, c, fill=SAND, stroke=AMBER, size=11, bold=True)
f.text(290, 224, "expected 5, got 4: the update of Thread 1 was lost", size=11, color=RED, bold=True)
f.text(290, 242, "fix: protect count++ and count-- with a mutex (critical section)", size=10, color=TEAL, bold=True)
```

```svgfig label="3.3" caption="A bounded buffer of N = 5 slots protected by three semaphores. empty counts free slots (starts at 5), full counts filled slots (starts at 0) and mutex (starts at 1) allows one process into the buffer at a time. The producer does wait(empty), wait(mutex), insert, signal(mutex), signal(full). The consumer does wait(full), wait(mutex), remove, signal(mutex), signal(empty). The snapshot shows three items inserted: empty = 2, full = 3, mutex = 1. If the buffer is full the producer sleeps on empty, and if it is empty the consumer sleeps on full."
f = Fig(580, 230)
f.box(10, 20, 100, 60, "Producer\nwait(empty)\nwait(mutex)", fill=SAND, stroke=AMBER, size=9.5, bold=True)
for i in range(5):
    f.box(150 + i * 54, 30, 50, 40, "item" if i < 3 else "", fill=BLUE if i < 3 else SOFT, stroke=NAVY, size=10, bold=True, r=0, dash=(i >= 3))
f.box(470, 20, 100, 60, "Consumer\nwait(full)\nwait(mutex)", fill=MINT, stroke=TEAL, size=9.5, bold=True)
f.arrow([(110, 50), (148, 50)], color=AMBER, sw=1.8)
f.arrow([(422, 50), (468, 50)], color=TEAL, sw=1.8)
f.text(285, 14, "buffer, N = 5", size=10.5, color=NAVY, bold=True)
f.box(40, 110, 150, 40, "empty = 2\n(free slots)", fill=SOFT, stroke=SLATE, size=10, bold=True)
f.box(215, 110, 150, 40, "full = 3\n(filled slots)", fill=SOFT, stroke=SLATE, size=10, bold=True)
f.box(390, 110, 150, 40, "mutex = 1\n(buffer unlocked)", fill=SOFT, stroke=SLATE, size=10, bold=True)
f.text(290, 178, "empty + full = 5 = N always", size=10.5, color=AMBER, bold=True)
f.text(290, 200, "swapping the two wait calls in the producer can deadlock the system", size=10, color=RED, bold=True)
f.text(290, 220, "(never wait(mutex) before wait(empty))", size=10, color=RED, bold=True)
```

```svgfig label="3.4" caption="Four schedules for the same four processes: P1 (arrival 0, burst 8), P2 (1, 4), P3 (2, 9) and P4 (3, 5). The Gantt charts are drawn to scale. FCFS gives average waiting time 8.75 and turnaround 15.25. Non-preemptive SJF gives 7.75 and 14.25. SRTF, the preemptive form, gives the best values, 6.50 and 13.00. Round robin with quantum 3 gives 13.50 and 20.00 but responds to every process within 9 time units and needs 9 context switches. Waiting time = turnaround time - burst time."
cols = {"P1": BLUE, "P2": MINT, "P3": SAND, "P4": ROSE}
edge = {"P1": NAVY, "P2": TEAL, "P3": AMBER, "P4": RED}
charts = [
 ("FCFS", [("P1",0,8),("P2",8,12),("P3",12,21),("P4",21,26)], "avg wait 8.75, turnaround 15.25"),
 ("SJF", [("P1",0,8),("P2",8,12),("P4",12,17),("P3",17,26)], "avg wait 7.75, turnaround 14.25"),
 ("SRTF", [("P1",0,1),("P2",1,5),("P4",5,10),("P1",10,17),("P3",17,26)], "avg wait 6.50, turnaround 13.00"),
 ("RR q=3", [("P1",0,3),("P2",3,6),("P3",6,9),("P4",9,12),("P1",12,15),("P2",15,16),("P3",16,19),("P4",19,21),("P1",21,23),("P3",23,26)], "avg wait 13.50, turnaround 20.00"),
]
f = Fig(580, 290)
S = 17
for k, (nm, segs, note) in enumerate(charts):
    y = 8 + k * 70
    f.text(8, y + 14, nm, size=10.5, color=NAVY, bold=True, anchor="start")
    for p, a, b in segs:
        f.box(70 + a * S, y, (b - a) * S, 28, p if b - a >= 2 else "", fill=cols[p], stroke=edge[p], size=9.5, bold=True, r=0)
    for t in sorted({s[1] for s in segs} | {26}):
        f.text(70 + t * S, y + 40, str(t), size=8.5, color=SLATE)
    f.text(70, y + 58, note, size=9.5, color=TEAL, bold=True, anchor="start")
```

```svgfig label="3.5" caption="Thread models. Many-to-one maps many user threads to one kernel thread: creation is cheap but one blocking call blocks all threads and there is no use of multiple cores. One-to-one gives each user thread its own kernel thread (Linux, Windows): true parallelism on a multicore CPU, at the cost of a kernel thread per user thread. Many-to-many multiplexes many user threads onto a smaller number of kernel threads, combining the benefits but being harder to build."
f = Fig(580, 230)
titles = ["Many-to-one", "One-to-one", "Many-to-many"]
xs = [10, 205, 400]
for t, x in zip(titles, xs):
    f.text(x + 85, 14, t, size=11, color=NAVY, bold=True)
    f.text(x + 85, 132, "kernel threads", size=9, color=SLATE)
for j in range(3):
    f.box(10 + j * 56, 30, 50, 28, "U%d" % (j + 1), fill=SAND, stroke=AMBER, size=10, bold=True)
    f.box(205 + j * 56, 30, 50, 28, "U%d" % (j + 1), fill=SAND, stroke=AMBER, size=10, bold=True)
    f.box(400 + j * 56, 30, 50, 28, "U%d" % (j + 1), fill=SAND, stroke=AMBER, size=10, bold=True)
f.box(65, 90, 50, 28, "K1", fill=BLUE, stroke=NAVY, size=10, bold=True)
for j in range(3):
    f.arrow([(35 + j * 56, 58), (90, 90)], color=SLATE, sw=1.2)
    f.box(205 + j * 56, 90, 50, 28, "K%d" % (j + 1), fill=BLUE, stroke=NAVY, size=10, bold=True)
    f.arrow([(230 + j * 56, 58), (230 + j * 56, 90)], color=SLATE, sw=1.2)
for j in range(2):
    f.box(430 + j * 70, 90, 50, 28, "K%d" % (j + 1), fill=BLUE, stroke=NAVY, size=10, bold=True)
for j in range(3):
    f.arrow([(425 + j * 56, 58), (455, 90)], color=SLATE, sw=1.2)
    f.arrow([(425 + j * 56, 58), (525, 90)], color=SLATE, sw=1.2)
f.text(90, 152, "one core only", size=10, color=RED, bold=True)
f.text(90, 168, "one block stops all", size=10, color=RED, bold=True)
f.text(285, 150, "parallel on many cores", size=10, color=TEAL, bold=True)
f.text(285, 168, "one kernel thread each", size=10, color=AMBER, bold=True)
f.text(490, 150, "flexible but complex", size=10, color=AMBER, bold=True)
f.text(290, 205, "Linux and Windows use one-to-one", size=10.5, color=NAVY, bold=True)
```

### 3.5.1 Eight advantages of multithreading

1. **Responsiveness.** A program can keep working while one thread waits for a slow job. A browser keeps scrolling while another thread downloads a page. The user never sees a frozen window.
2. **Resource sharing.** Threads of one process share code, data and open files by default. They can exchange data through ordinary variables, without system calls. This is much easier than message passing between separate processes.
3. **Economy.** Creating a thread and switching between threads costs much less than doing the same for processes, because the memory map does not change. A web server can start a thread for every request in microseconds. This is how a result website survives thousands of students checking marks at once.
4. **Use of multiple cores.** A multithreaded program can run its threads on different cores at the same time. A video converter that splits a movie into four parts finishes almost four times faster on four cores. A single-threaded program leaves the other cores idle.
5. **Simple program structure.** Different jobs, such as reading input, calculating and drawing, can each be written as a thread. Each thread contains simple sequential code. This is easier to understand than one large loop that does everything.
6. **Better use of the CPU during I/O.** While one thread waits for the disk or network, another thread of the same process uses the CPU. Throughput rises without more hardware. A Fonepay server that waits for a bank reply can serve other customers in the meantime.
7. **Scalability.** Programs written with threads can take advantage of more cores when the hardware is upgraded. A server with 32 cores can run 32 worker threads without any change in design. The same code serves a small college lab and a national portal.
8. **Background services.** Threads suit tasks such as auto-save, spell checking, logging and garbage collection. They run quietly beside the main job. A word processor saving a thesis every minute is an example.

## Formula and fact sheet

- **TAT = CT − AT; WT = TAT − BT; response = first run − AT.**
- Process states: new, ready, running, waiting, terminated. Running → waiting on I/O; waiting → ready on completion.
- Critical section needs mutual exclusion, progress, bounded waiting.
- Semaphore: down = wait/P; up = signal/V. Bounded buffer: mutex = 1, empty = N, full = 0.
- Peterson: `flag[i] = true; turn = j; while (flag[j] && turn == j);`
- SJF minimises average waiting; SRTF is its preemptive form; RR with large *q* → FCFS.
- Exponential average: τₙ₊₁ = αtₙ + (1 − α)τₙ. RMS bound n(2^(1/n) − 1); EDF bound 1.
- Conflict-serializable ⇔ precedence graph is acyclic.

## Chapter summary

- A process is a program in execution described by a PCB; it moves among new, ready, running, waiting and terminated; `fork`, `exec`, `wait` and `exit` manage it.
- Threads share the address space but have their own stacks and registers; one-to-one is the dominant model.
- Unsynchronised access to shared data creates race conditions; the critical-section solution needs mutual exclusion, progress and bounded waiting. Peterson and TSL use busy waiting; semaphores, monitors and message passing block instead.
- The classical problems (bounded buffer, dining philosophers, readers-writers, sleeping barber) are templates for real synchronization bugs. Two-phase locking and timestamps give serializable transaction schedules.
- Scheduling algorithms trade throughput, turnaround, waiting and response time: SJF/SRTF minimise waiting, RR gives fairness, MLFQ adapts, RMS/EDF handle deadlines.

## Practice

1. Draw the five-state process diagram and state the cause of every transition.
2. What does a PCB contain? Why is a context switch considered overhead?
3. After `pid = fork()`, what does each of the parent and child receive? Why can the parent's variable stay unchanged when the child modifies its copy?
4. Differentiate a process and a thread. Which resources are shared among the threads of one process?
5. Explain many-to-one, one-to-one and many-to-many models with one drawback each.
6. What is a race condition? Show how `counter++` by two threads can lose an update.
7. State the three requirements of a critical-section solution. Why does the plain lock variable fail?
8. Explain Peterson's solution and show that it provides mutual exclusion.
9. Write semaphore pseudo-code for the bounded buffer and explain what happens if the two `down` calls in the producer are swapped.
10. Describe how the dining philosophers deadlock can occur and give two solutions.
11. Compute average waiting time for FCFS and SJF for processes arriving at 0 with bursts P1 = 6, P2 = 8, P3 = 7, P4 = 3.
12. Round robin, *q* = 2, arrivals at 0: P1 = 5, P2 = 3, P3 = 1. Draw the Gantt chart and find the average TAT.
13. Test whether R1(A) W2(A) W1(A) R2(B) W2(B) R1(B) is conflict-serializable.
14. Three real-time tasks have (C, T) = (2, 5), (2, 7), (3, 10). Is RMS guaranteed to schedule them by the utilisation test?

::: note Answers and worked solutions
**1.** New → Ready (admitted); Ready → Running (dispatched); Running → Ready (quantum expired / preempted); Running → Waiting (waits for I/O or event); Waiting → Ready (event done); Running → Terminated (exit or killed).
**2.** PID, state, program counter, registers, scheduling info, memory-management info (page table), accounting, open files/I/O status. During a switch the CPU does no user work and the caches and TLB lose useful content, so it is pure overhead.
**3.** The parent receives the child's PID (> 0); the child receives 0 (−1 means failure). The child has a *copy* of the address space (copy-on-write), so a write by the child goes to its own copy.
**4.** A process is a program in execution with its own address space and resources; a thread is a unit of execution inside a process. Threads of one process share code, data, heap, open files and signal handlers; each has its own registers, program counter and stack.
**5.** Many-to-one: all threads in one kernel thread, so one blocking call blocks all. One-to-one: each user thread has a kernel thread, which is expensive in kernel resources if there are thousands. Many-to-many: *m* user to *n* kernel threads, but hard to implement.
**6.** A race condition is a result that depends on the interleaving of unsynchronised accesses to shared data. With counter = 5: T1 loads 5; T2 loads 5; T1 stores 6; T2 stores 6. Two increments produced +1.
**7.** Mutual exclusion, progress, bounded waiting. A lock variable fails because test and set are separate steps: P0 reads 0, is pre-empted, P1 reads 0 and sets 1, enters; P0 resumes, sets 1 and also enters.
**8.** A process sets `flag[i] = true` and `turn = j`, then waits while `flag[j] && turn == j`. If both are in their critical sections, both flags are true, so each must have seen `turn` pointing to itself, but `turn` holds only one value (the last write), a contradiction. Hence mutual exclusion; bounded waiting follows because after one entry the other process sets `turn` to give way.
**9.** `down(empty); down(mutex); insert; up(mutex); up(full)`. If swapped, a producer can take `mutex`, find the buffer full and sleep on `empty`; the consumer needs `mutex` to remove an item, so both wait forever: **deadlock**.
**10.** If all five take their left fork, each holds one fork and waits for the neighbour's: circular wait. Solutions: at most four philosophers at the table; take both forks atomically; order the forks (lower number first), which breaks circular wait; an asymmetric rule (odd philosophers pick left first, even right first).
**11.** FCFS order P1, P2, P3, P4: waits 0, 6, 14, 21: average **10.25**. SJF order P4, P1, P3, P2: waits 0, 3, 9, 16: average **7.00**.
**12.** Gantt: P1[0–2] P2[2–4] P3[4–5] P1[5–7] P2[7–8] P1[8–9]. Completion: P1 = 9, P2 = 8, P3 = 5. TAT = 9, 8, 5, average **7.33**.
**13.** Conflicts: R1(A) before W2(A): T1 → T2; W2(A) before W1(A): T2 → T1. Cycle, so **not** conflict-serializable.
**14.** U = 2/5 + 2/7 + 3/10 = 0.4 + 0.2857 + 0.3 = 0.9857. The bound for n = 3 is 0.7798. Since 0.9857 > 0.7798 the *sufficient* test fails; RMS is **not guaranteed** (the test is not necessary, so one would then run an exact analysis), but EDF's bound is U ≤ 1 and holds.
:::

## Model answers (5 and 10 marks)

**Q1. Distinguish between a program and a process. Explain the states of a process with a diagram. (5 marks)**

A **program** is a passive file of instructions stored on disk, for example `a.out`. A **process** is a program in execution: it has a program counter, registers, a stack, a heap, a data section and a **process control block (PCB)** that the OS keeps for it. Opening the same editor twice creates two processes of one program.

A process passes through five **states** (Figure 3.1):

1. **New:** the process is being created and its PCB is built.
2. **Ready:** it is loaded and waits in the ready queue for the CPU.
3. **Running:** the CPU is executing its instructions.
4. **Waiting (blocked):** it waits for an event such as I/O completion.
5. **Terminated:** it has finished and its resources are released.

The transitions are: admit (new to ready), dispatch (ready to running, by the scheduler), timeout (running to ready, when the time slice ends), I/O request (running to waiting), I/O completion (waiting to ready) and exit (running to terminated). Note that a waiting process never goes directly to running; it must first queue in the ready state.

The PCB stores the state, program counter, CPU registers, scheduling information, memory limits and open files, so that the OS can stop and later resume the process by a **context switch**.

**Q2. Differentiate between a process and a thread. Explain the multithreading models. (5 marks)**

A **thread** is a unit of CPU execution inside a process. It has its own program counter, registers and stack but shares the code, data and open files of its process. A process with several threads can do several things at once.

| Point | Process | Thread |
|---|---|---|
| Memory | own address space | shares the address space |
| Creation cost | high | low |
| Context switch | slow (memory map changes) | fast |
| Communication | IPC needed | shared variables |
| Failure | isolated from others | can crash the whole process |

**Models (Figure 3.5).** In **many-to-one**, many user threads share one kernel thread; it is cheap but a blocking call blocks all threads and only one core is used. In **one-to-one**, each user thread has its own kernel thread, giving real parallelism at the cost of more kernel resources; Linux and Windows use it. In **many-to-many**, many user threads are multiplexed over a smaller number of kernel threads, which is flexible but complex.

**Q3. What is a race condition? Explain the critical section problem and solve the producer-consumer problem with semaphores. (10 marks)**

**Introduction.** When several processes or threads read and write shared data and the final result depends on the order in which they run, the situation is a **race condition**. In Figure 3.2 two threads execute `count++` and `count--` on count = 5. Both load 5, one stores 6, the other stores 4, and the result is 4 instead of 5.

**Critical section problem.** The part of the code that touches shared data is the **critical section**. A correct solution must satisfy three requirements:

1. **Mutual exclusion:** only one process is inside its critical section at a time.
2. **Progress:** if no process is inside, a process that wants to enter cannot be postponed forever by processes outside.
3. **Bounded waiting:** a limit exists on how many times others may enter before a waiting process gets its turn.

Software solutions such as Peterson's algorithm and hardware support such as test-and-set meet these requirements, but busy waiting wastes CPU time. The usual tool is the **semaphore**, an integer with two atomic operations: `wait(S)` (P) decrements S and blocks if S is already 0, and `signal(S)` (V) increments S and wakes one waiting process.

**Producer-consumer with a buffer of N slots.**

```text
semaphore mutex = 1, empty = N, full = 0

Producer:                 Consumer:
  wait(empty)               wait(full)
  wait(mutex)               wait(mutex)
  insert item               remove item
  signal(mutex)             signal(mutex)
  signal(full)              signal(empty)
```

`empty` counts free slots, so the producer sleeps when the buffer is full. `full` counts items, so the consumer sleeps when it is empty. `mutex` makes the insertion and removal atomic. If the producer called `wait(mutex)` before `wait(empty)`, it could hold the mutex while sleeping and the consumer could never enter: a deadlock. Figure 3.3 shows the buffer with N = 5 and three items (empty = 2, full = 3, mutex = 1).

| Tool | Idea | Weakness |
|---|---|---|
| Lock variable | simple flag | not atomic |
| Peterson | two processes, shared turn | busy waiting |
| Semaphore | counter with sleep and wakeup | easy to misorder |
| Monitor | language-level lock | needs language support |

**Conclusion.** Race conditions are prevented by making critical sections mutually exclusive, and semaphores do this without wasting CPU time.

**Q4. Explain the CPU scheduling algorithms FCFS, SJF, SRTF and Round Robin. Compare them with the data P1 (0, 8), P2 (1, 4), P3 (2, 9), P4 (3, 5). (10 marks)**

**Introduction.** The scheduler chooses which ready process receives the CPU. Common criteria are CPU utilisation, throughput, turnaround time (completion minus arrival), waiting time (turnaround minus burst) and response time.

**FCFS** serves processes in arrival order and is non-preemptive. It is simple but short jobs wait behind a long one (the convoy effect). **SJF** picks the ready process with the shortest burst; it gives the minimum average waiting time among non-preemptive methods but may starve long jobs and needs a burst estimate. **SRTF** is the preemptive SJF: a new arrival with a shorter remaining time takes the CPU. **Round robin** gives each process a quantum and puts it at the rear of the queue when the quantum expires; it is fair and has good response time, but a very small quantum wastes time in context switches and a very large one behaves like FCFS.

**Worked result (Figure 3.4).** The Gantt charts give:

| Algorithm | Order of execution | Average waiting | Average turnaround |
|---|---|---|---|
| FCFS | P1, P2, P3, P4 | 8.75 | 15.25 |
| SJF | P1, P2, P4, P3 | 7.75 | 14.25 |
| SRTF | P1, P2, P4, P1, P3 | 6.50 | 13.00 |
| RR, q = 3 | P1, P2, P3, P4, P1, ... | 13.50 | 20.00 |

For SRTF, P2 arrives at time 1 with burst 4 and preempts P1 (remaining 7), then P4 (5) runs before P1 resumes. Waiting times are P1 = 9, P2 = 0, P3 = 15, P4 = 2, total 26, average 6.50.

**Conclusion.** SRTF minimises average waiting but needs predictions and can starve long jobs. Round robin has the worst averages here but serves every process within 9 time units, which is why time-sharing systems use it.

**Q5. A round-robin scheduler uses a time quantum of 3. Draw the Gantt chart for P1 (0, 8), P2 (1, 4), P3 (2, 9), P4 (3, 5) and find the average waiting time and turnaround time. (5 marks)**

**Method.** Processes wait in a queue. Each runs for at most 3 units; an unfinished process goes to the rear, after any process that arrived during its slice.

**Gantt chart:**

| P1 | P2 | P3 | P4 | P1 | P2 | P3 | P4 | P1 | P3 |
|---|---|---|---|---|---|---|---|---|---|
| 0-3 | 3-6 | 6-9 | 9-12 | 12-15 | 15-16 | 16-19 | 19-21 | 21-23 | 23-26 |

**Completion, turnaround (TAT = completion - arrival) and waiting (WT = TAT - burst):**

| Process | Arrival | Burst | Completion | TAT | WT |
|---|---|---|---|---|---|
| P1 | 0 | 8 | 23 | 23 | 15 |
| P2 | 1 | 4 | 16 | 15 | 11 |
| P3 | 2 | 9 | 26 | 24 | 15 |
| P4 | 3 | 5 | 21 | 18 | 13 |

Average waiting time = (15 + 11 + 15 + 13) / 4 = 54 / 4 = **13.5**. Average turnaround time = (23 + 15 + 24 + 18) / 4 = 80 / 4 = **20.0**. There are 10 slices and so 9 context switches. Every process gets the CPU for the first time by time 9, so the response time is good even though the averages are poor.
