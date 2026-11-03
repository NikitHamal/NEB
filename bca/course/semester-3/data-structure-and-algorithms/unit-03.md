---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 3
title: Queue
hours: 3
area: BCA 201 · Data Structure and Algorithms · Unit 3
---

A **queue** is a linear structure where items are added at one end (the **rear**) and removed from the other (the **front**): **FIFO**, first in, first out. It models any fair waiting line.

::: key What this unit gives you
- The Queue ADT and the primitive operations enqueue and dequeue.
- Why a simple linear queue wastes space and how a **circular queue** fixes it.
- The priority queue and the double-ended queue.
- Tested C code and typical applications.
:::

## 3.1 Queue as an ADT

| Operation | Effect |
|---|---|
| `enqueue(x)` | add x at the rear; **overflow** if full |
| `dequeue()` | remove and return the front item; **underflow** if empty |
| `front()` | read the front without removing |
| `isEmpty()`, `isFull()` | state tests |

### Linear queue (array)

Keep `front` and `rear`. Initially `front = 0`, `rear = −1`. Enqueue: `items[++rear] = x`. Dequeue: `items[front++]`. Empty when `front > rear`; full when `rear == MAX − 1`.

**The flaw.** After 5 enqueues and 5 dequeues in a queue of size 5, `rear == MAX − 1`, so the queue reports *full* although every cell is free. The cells to the left of `front` are wasted forever. Shifting everything left after each dequeue works but costs O(n).

### Circular queue

Treat the array as a ring: after index MAX − 1 comes index 0. Advance with **modulo**: `rear = (rear + 1) % MAX`, `front = (front + 1) % MAX`. To tell full from empty, keep a **count** of items (or sacrifice one cell).

::: example Worked example: circular queue, MAX = 4
Start: count 0, front 0, rear 3 (so the first enqueue goes to index 0).
enqueue A → idx 0; B → idx 1; C → idx 2 (count 3). dequeue → A (front 1, count 2). enqueue D → idx 3; enqueue E → rear wraps to idx 0 (count 4, full). enqueue F → **overflow**. The array holds [E B C D] but the queue order is B, C, D, E: the logical order follows `front`, not the array order.
:::

## 3.2 Program: circular queue and priority queue

```c
#include <stdio.h>
#define MAX 4

typedef struct { int a[MAX]; int front, rear, count; } CQ;

void cq_init(CQ *q) { q->front = 0; q->rear = MAX - 1; q->count = 0; }
int  cq_enq(CQ *q, int x) {
    if (q->count == MAX) { printf("Overflow: %d rejected\n", x); return 0; }
    q->rear = (q->rear + 1) % MAX;
    q->a[q->rear] = x; q->count++;
    return 1;
}
int cq_deq(CQ *q, int *x) {
    if (q->count == 0) return 0;
    *x = q->a[q->front]; q->front = (q->front + 1) % MAX; q->count--;
    return 1;
}

/* Priority queue: smaller number = higher priority; kept sorted on insertion */
typedef struct { int item[10], pri[10], n; } PQ;
void pq_insert(PQ *q, int item, int pri) {
    int i = q->n - 1;
    while (i >= 0 && q->pri[i] > pri) { q->item[i+1] = q->item[i]; q->pri[i+1] = q->pri[i]; i--; }
    q->item[i+1] = item; q->pri[i+1] = pri; q->n++;
}

int main(void) {
    CQ q; int x; cq_init(&q);
    cq_enq(&q, 1); cq_enq(&q, 2); cq_enq(&q, 3);
    cq_deq(&q, &x); printf("dequeued %d\n", x);
    cq_enq(&q, 4); cq_enq(&q, 5); cq_enq(&q, 6);      /* 6 overflows */
    printf("front=%d rear=%d count=%d; array = [%d %d %d %d]\n",
           q.front, q.rear, q.count, q.a[0], q.a[1], q.a[2], q.a[3]);
    printf("order:");
    while (cq_deq(&q, &x)) printf(" %d", x);
    printf("\n");

    PQ p = {{0},{0},0};
    pq_insert(&p, 100, 3); pq_insert(&p, 200, 1); pq_insert(&p, 300, 2); pq_insert(&p, 400, 1);
    printf("priority order:");
    for (int i = 0; i < p.n; i++) printf(" %d(p%d)", p.item[i], p.pri[i]);
    printf("\n");
    return 0;
}
```
```output
dequeued 1
Overflow: 6 rejected
front=1 rear=0 count=4; array = [5 2 3 4]
order: 2 3 4 5
priority order: 200(p1) 400(p1) 300(p2) 100(p3)
```

## 3.3 Priority queue and deque

A **priority queue** serves the item with the highest priority first; items of equal priority are served in arrival order. Implementations: an **ordered array/list** (insert O(n), remove O(1)), an **unordered** one (insert O(1), remove O(n)), or a **heap** (both O(log n), Unit 8). Uses: CPU scheduling, hospital triage, Dijkstra's algorithm, event simulation.

A **double-ended queue (deque)** allows insertion and deletion at both ends. An **input-restricted** deque inserts at one end only; an **output-restricted** deque deletes at one end only. A deque can act as both a stack and a queue.

## 3.4 Applications of queues

- **CPU scheduling** (round robin), **printer spooling**, keyboard buffers.
- **Breadth-first search** of trees and graphs (Unit 10).
- **Simulation** of waiting lines (bank counters, traffic).
- **Buffering** in streaming and network packets: producers enqueue, consumers dequeue at their own speed.
- **Level-order traversal** of a binary tree (Unit 7).

::: caution Common mistakes
With `front`/`rear` only (no count), a circular queue cannot tell full from empty because both give `front == (rear + 1) % MAX`. Use a counter or leave one cell unused (then capacity is MAX − 1).
:::

## 3.5 Seeing the ideas: queues in life and in memory

Queues are so familiar that we hardly notice them: the line at a railway ticket counter, the cars waiting at a traffic light, the documents waiting for the printer. In each case the person who arrived first is served first. The photograph shows such a queue at a ticket window, and the figures translate it into arrays, indices and priorities.

```photogrid label="3.1" cols="2" ratio="1.2" caption="A queue is first in, first out. (a) People wait at a railway ticket window: new arrivals join at the rear, and the person at the front is served and leaves. (b) The same rule in memory: a circular array of size 5. After enqueuing A to E, dequeuing A and B, and enqueuing F and G, the items wrap around to cells 0 and 1, front is 2, rear is 1 and the queue is full again with count 5."
@ photo id="bca201/queue" cap="A ticket queue: front is served first"
fit 1.2
focus 0.5 0.5
call 0.28 0.5 0.04 0.9 "rear: new arrivals join here"
@ svg cap="Circular queue of size 5 after wrap-around"
f = Fig(300, 250)
f.text(150, 14, "MAX = 5, count = 5 (full)", size=10.5, color=NAVY, bold=True)
vals = ["F", "G", "C", "D", "E"]
for i, v in enumerate(vals):
    x = 20 + i * 52
    f.box(x, 70, 48, 44, v, fill=SAND if i < 2 else BLUE, stroke=AMBER if i < 2 else NAVY, size=14, bold=True, r=0)
    f.text(x + 24, 130, "[%d]" % i, size=10, color=SLATE)
f.arrow([(124, 44), (124, 70)], color=TEAL, sw=1.8)
f.text(124, 36, "front = 2", size=10.5, color=TEAL, bold=True)
f.arrow([(72, 200), (72, 116)], color=RED, sw=1.8)
f.text(72, 214, "rear = 1", size=10.5, color=RED, bold=True)
f.text(150, 160, "rear = (rear + 1) % 5", size=10.5, color=SLATE, bold=True)
f.text(150, 180, "front = (front + 1) % 5", size=10.5, color=SLATE, bold=True)
f.text(150, 240, "F and G reused the cells freed by A and B", size=9.5, color=AMBER, bold=True)
```

```svgfig label="3.1" caption="Why a linear array queue is not enough. In a linear queue of size 5 the rear index only moves right. After five enqueues and three dequeues, only two items remain (D and E) but rear is 4, so the queue reports that it is full even though three cells at the left are empty. This is called false overflow. The circular queue of Plate 3.1(b) avoids it by wrapping the index back to 0 using the modulus operator."
f = Fig(580, 170)
f.text(290, 14, "Linear queue: 5 enqueues, 3 dequeues, then enqueue(F)", size=10.5, color=NAVY, bold=True)
cells = ["", "", "", "D", "E"]
for i, v in enumerate(cells):
    x = 120 + i * 62
    f.box(x, 40, 58, 40, v, fill=BLUE if v else SOFT, stroke=NAVY, size=13, bold=True, r=0, dash=(not v))
    f.text(x + 29, 96, "[%d]" % i, size=10, color=SLATE)
f.arrow([(208, 130), (208, 84)], color=TEAL, sw=1.6)
f.text(208, 142, "front = 3", size=10, color=TEAL, bold=True)
f.arrow([(394, 130), (394, 84)], color=RED, sw=1.6)
f.text(394, 142, "rear = 4 = MAX - 1", size=10, color=RED, bold=True)
f.box(10, 52, 100, 36, "enqueue(F)\nrejected", fill=ROSE, stroke=RED, size=10, bold=True)
f.text(290, 162, "three free cells wasted: false overflow", size=10.5, color=RED, bold=True)
```

```svgfig label="3.2" caption="Two extensions of the queue. (a) A priority queue serves the item with the highest priority first; here a smaller number means more urgent. Four patients arrive in the order Hari (3), Sita (1), Ram (2), Gita (1) and are served in the order Sita, Gita, Ram, Hari; Sita is ahead of Gita because equal priorities are served in arrival order. (b) A double-ended queue (deque) allows insertion and deletion at both ends, so it can behave as a stack or as a queue."
f = Fig(580, 230)
f.text(145, 14, "(a) Priority queue (smaller = more urgent)", size=10.5, color=NAVY, bold=True)
for i, (nm, pr) in enumerate([("Hari", 3), ("Sita", 1), ("Ram", 2), ("Gita", 1)]):
    f.box(10 + i * 70, 30, 64, 34, "%s\n(%d)" % (nm, pr), fill=SOFT, stroke=SLATE, size=10, bold=True)
f.text(145, 80, "arrival order", size=9.5, color=SLATE)
f.arrow([(145, 90), (145, 112)], color=TEAL, sw=1.6)
for i, (nm, pr) in enumerate([("Sita", 1), ("Gita", 1), ("Ram", 2), ("Hari", 3)]):
    f.box(10 + i * 70, 120, 64, 34, "%s\n(%d)" % (nm, pr), fill=MINT, stroke=TEAL, size=10, bold=True)
f.text(145, 172, "service order", size=9.5, color=TEAL, bold=True)
f.text(435, 14, "(b) Deque (double-ended queue)", size=10.5, color=NAVY, bold=True)
for i, v in enumerate(["12", "7", "30", "5"]):
    f.box(350 + i * 52, 70, 48, 40, v, fill=BLUE, stroke=NAVY, size=12, bold=True, r=0)
f.text(374, 54, "insert/delete\nfront", size=9, color=RED, bold=True)
f.text(530, 54, "insert/delete\nrear", size=9, color=RED, bold=True)
f.text(435, 140, "input-restricted: insert at one end only", size=9.5, color=SLATE)
f.text(435, 158, "output-restricted: delete at one end only", size=9.5, color=SLATE)
f.text(290, 215, "queue = deque with insert at rear and delete at front; stack = deque used at one end", size=9.5, color=AMBER, bold=True)
```

### 3.5.1 Eight applications of queues

1. **Printer and job spooling.** When many users send documents to one printer in a college lab, the spooler places the jobs in a queue and prints them in arrival order. No job is lost and none jumps ahead. The same idea is used for batch jobs on a shared server.
2. **CPU scheduling.** An operating system keeps the ready processes in a queue. In round-robin scheduling the process at the front gets a short time slice and then goes to the rear. Every process receives a fair share of the processor.
3. **Bank and ticket counters.** A bank token display or an online ticket system serves customers strictly in the order of arrival. The counter staff call the front token and the token is removed. A queue gives the fairness people expect.
4. **Payment and message handling.** Servers behind ConnectIPS, Fonepay and eSewa receive thousands of requests per second on festival evenings such as Dashain shopping. They place the requests in a queue so that bursts are absorbed and each one is processed in order. This prevents overload and loss of transactions.
5. **Buffers for input and output.** Keyboard characters, network packets and streaming video are stored in a queue until the program or the screen is ready. The circular queue is the usual buffer because it reuses space. This makes video playing smooth even when the internet speed varies.
6. **Breadth-first search.** To explore a graph or a maze level by level, the algorithm keeps the discovered vertices in a queue (Unit 10). The vertex that was discovered first is expanded first. This guarantees the shortest path in an unweighted graph.
7. **Priority servicing.** A hospital emergency ward and an operating system serve urgent items first by using a priority queue (Figure 3.2). Equal priorities are served in arrival order. This protects critical work from long waits.
8. **Simulation of waiting lines.** Planners simulate bus stops, toll plazas and airport check-in with queues to estimate waiting time and the number of counters needed. The result helps them to decide how many counters to open at a place like the Tribhuvan International Airport. A queue is the model of any service system.

## Formula and fact sheet

- Queue is FIFO; enqueue at rear, dequeue at front; both O(1).
- Linear queue full: `rear == MAX − 1`; empty: `front > rear`.
- Circular: `rear = (rear + 1) % MAX`; full when `count == MAX`.
- Priority queue by heap: insert and remove O(log n).
- Deque: both ends; input- or output-restricted variants.

## Chapter summary

- A queue gives first-come-first-served access with O(1) operations.
- The linear array queue wastes cells; the circular queue reuses them with modulo arithmetic.
- Priority queues break FIFO by priority; deques allow both ends.
- Queues drive scheduling, buffering and BFS.

## Practice

1. Define queue and state the conditions for overflow and underflow in a linear and a circular queue.
2. A linear queue of size 5 has had 5 enqueues and 3 dequeues. Is it full? How many items does it hold? What is the drawback?
3. Trace a circular queue of size 4 under: enq 10, enq 20, enq 30, deq, enq 40, enq 50, enq 60. Give final front, rear, count.
4. Distinguish between a queue and a priority queue with an example.
5. What is a deque? Name its two restricted forms.
6. Why does a circular queue need a count (or a spare cell)?
7. Describe how a stack can be built from two queues.
8. List four applications of a queue.

::: note Answers and worked solutions
**1.** Queue: FIFO list with enqueue at rear and dequeue at front. Linear: overflow if `rear == MAX−1`, underflow if `front > rear`. Circular: overflow if count == MAX, underflow if count == 0.
**2.** `rear == MAX − 1`, so it reports **full**, yet it holds 2 items (5 − 3). Three cells at the left are free but unusable: the wasted-space drawback.
**3.** Start front 0, rear 3, count 0. enq 10, 20, 30 → idx 0, 1, 2, count 3. deq → 10, front 1, count 2. enq 40 → idx 3, count 3. enq 50 → rear wraps to idx 0, count 4. enq 60 → **overflow**. Final: front = 1, rear = 0, count = 4; queue order 20, 30, 40, 50.
**4.** A queue serves by arrival time (a ticket line); a priority queue serves by priority (an emergency patient is treated before an earlier routine patient).
**5.** A double-ended queue supports insert and delete at both ends. Input-restricted and output-restricted.
**6.** With only `front` and `rear`, a full queue and an empty queue produce the same relation between them, so one extra piece of information is needed.
**7.** Push: enqueue into Q1. Pop: move all but the last item from Q1 to Q2, dequeue the last one from Q1 as the result, then swap the names of Q1 and Q2. (Pop is O(n).)
**8.** CPU scheduling, print spooling, BFS, keyboard/network buffering.
:::

## Model answers (5 and 10 marks)

**Q1. Define a queue. Explain its operations and differentiate it from a stack. (5 marks)**

A **queue** is a linear data structure in which items are inserted at one end, the **rear**, and deleted from the other end, the **front**. It follows the **FIFO** rule (first in, first out): the item that has waited longest is served first, as in the ticket line of Plate 3.1.

**Operations**
1. `enqueue(x)`: insert x at the rear; fails with *overflow* if the queue is full.
2. `dequeue()`: remove and return the item at the front; fails with *underflow* if the queue is empty.
3. `peek()`: read the front item without removing it.
4. `isEmpty()` and `isFull()`: test the state.

| Point | Stack | Queue |
|---|---|---|
| Rule | LIFO | FIFO |
| Insertion | at the top | at the rear |
| Deletion | from the top | from the front |
| Pointers | one (top) | two (front and rear) |
| Typical use | undo, recursion | scheduling, buffers |

For example, after `enqueue(A)`, `enqueue(B)` and `enqueue(C)`, a call to `dequeue()` returns A, not C. The stack would return C. With two pointers, a queue needs a little more bookkeeping than a stack, but both operations are O(1).

**Q2. What is the drawback of a linear queue? How does a circular queue solve it? (5 marks)**

In a linear queue made from an array, `rear` moves right at every `enqueue` and `front` moves right at every `dequeue`, but neither moves back. When `rear` reaches `MAX - 1` the queue is declared full, even if many cells at the left have been freed by earlier dequeues. For example, with MAX = 5, after five enqueues and three dequeues the items D and E occupy cells 3 and 4, `rear` is 4, and `enqueue(F)` is refused although three cells are empty. This wasted space is called **false overflow** (Figure 3.1).

A **circular queue** treats the array as a ring whose last cell is followed by the first. The indices wrap around by the modulus operator:

- `rear = (rear + 1) % MAX` on `enqueue`;
- `front = (front + 1) % MAX` on `dequeue`.

A counter `count` records the number of items, so the queue is full when `count == MAX` and empty when `count == 0`. (Without the counter, the full and empty cases would look alike.) In Plate 3.1(b) the items F and G reuse cells 0 and 1 freed by A and B, so all five cells are in use.

The circular queue therefore uses the whole array with the same O(1) operations, which is why it is used for buffers and schedulers.

**Q3. Explain the circular queue with algorithms and a worked trace, and describe the priority queue and the deque. (10 marks)**

**Introduction.** A queue is a FIFO list. The array version needs a circular arrangement to avoid false overflow. Variants such as the priority queue and the deque relax the strict FIFO rule.

**Circular queue.** Data: `int q[MAX]; int front = 0, rear = -1, count = 0;`

*Enqueue(x):* (1) if `count == MAX`, report overflow and stop; (2) `rear = (rear + 1) % MAX`; (3) `q[rear] = x`; (4) `count = count + 1`.

*Dequeue():* (1) if `count == 0`, report underflow and stop; (2) `x = q[front]`; (3) `front = (front + 1) % MAX`; (4) `count = count - 1`; (5) return x.

**Trace (MAX = 5, Plate 3.1b).** Enqueue A, B, C, D, E: the items go to cells 0 to 4, `rear = 4`, `count = 5`, the queue is full. Dequeue twice: A and B leave, `front = 2`, `count = 3`. Enqueue F: `rear = (4 + 1) % 5 = 0`, so F goes to cell 0. Enqueue G: `rear = 1`, G goes to cell 1 and `count = 5`. The queue content from front to rear is C, D, E, F, G.

**Priority queue.** Each item carries a priority and the item with the highest priority is removed first; equal priorities follow FIFO order. With patients Hari (3), Sita (1), Ram (2), Gita (1), where 1 is most urgent, the service order is Sita, Gita, Ram, Hari (Figure 3.2a). It can be implemented by an ordered list (insertion O(n), removal O(1)) or by a heap (both O(log n), Unit 8).

**Deque.** A double-ended queue allows insertion and deletion at both ends (Figure 3.2b). An *input-restricted* deque inserts at one end only; an *output-restricted* deque deletes at one end only. It can act as a stack or as a queue.

| Type | Insert | Delete | Order served | Use |
|---|---|---|---|---|
| Linear queue | rear | front | arrival | simple buffers |
| Circular queue | rear (wraps) | front (wraps) | arrival | I/O buffers, scheduling |
| Priority queue | by priority | highest priority | urgency | hospital, OS tasks |
| Deque | both ends | both ends | flexible | undo/redo, sliding window |

**Conclusion.** The queue models fair service. The circular form removes the waste of the linear array, the priority queue serves urgent work first and the deque gives the flexibility of both a stack and a queue; all basic operations remain O(1) except the priority queue, which needs O(log n) with a heap.
