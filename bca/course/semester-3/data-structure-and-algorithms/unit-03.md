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
