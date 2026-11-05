---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 4
title: List
hours: 2
area: BCA 201 · Data Structure and Algorithms · Unit 4
---

A **list** is a finite, ordered sequence of items in which an item can be inserted or removed at *any* position, not only at the ends. Stacks and queues are restricted lists; the list is the general case.

::: key What this unit gives you
- The List ADT and its operations.
- Static (array) versus dynamic (pointer) list structures, with their costs.
- Array implementation with shifting, in tested C.
- How a queue is a special list.
:::

## 4.1 The List ADT

| Operation | Meaning |
|---|---|
| `insert(pos, x)` | put x so that it becomes the item at position `pos`; later items move up |
| `delete(pos)` | remove the item at `pos`; later items move down |
| `get(pos)` / `set(pos, x)` | read / change the item at `pos` |
| `search(x)` | position of x, or "not found" |
| `length()`, `isEmpty()`, `isFull()` | state |
| `traverse()` | visit every item in order |

## 4.2 Static and dynamic list structures

| | **Static (array-based)** | **Dynamic (linked)** |
|---|---|---|
| Storage | one contiguous block of fixed size | separate nodes joined by pointers |
| Access by position | **O(1)** | O(n), must walk from the head |
| Insert/delete in the middle | O(n), items must be shifted | O(1) once the place is found |
| Memory | wasted if under-filled; overflow if full | exactly as needed + a pointer per node |
| Size change | fixed (or reallocate and copy) | grows and shrinks freely |

The linked implementation is the subject of Unit 5. Here we study the array list.

## 4.3 Array implementation of a list

Store items in `a[0..n−1]`, with `n` the current length.

**Insert at position p (0-based):** if `n == MAX` report overflow; move `a[n−1], …, a[p]` one place right (start from the end); store x at `a[p]`; `n++`.
**Delete at position p:** if `p` is invalid report an error; move `a[p+1], …, a[n−1]` one place left (start from the front); `n−−`.

::: example Worked example: insert and delete
List [10, 20, 30, 40], n = 4. Insert 25 at position 2: shift 40 → index 4, 30 → index 3, then place 25 at index 2: **[10, 20, 25, 30, 40]**. Delete position 0: shift 20, 25, 30, 40 one left: **[20, 25, 30, 40]**. Insert at the end needs no shifting (O(1)); insert at the front shifts everything (O(n)). Average cost of a random insertion or deletion is about n/2 moves.
:::

```c
#include <stdio.h>
#define MAX 8

typedef struct { int a[MAX]; int n; } List;

int insert_at(List *L, int p, int x) {
    if (L->n == MAX || p < 0 || p > L->n) return 0;
    for (int i = L->n - 1; i >= p; i--) L->a[i + 1] = L->a[i];
    L->a[p] = x; L->n++;
    return 1;
}
int delete_at(List *L, int p) {
    if (p < 0 || p >= L->n) return 0;
    for (int i = p; i < L->n - 1; i++) L->a[i] = L->a[i + 1];
    L->n--;
    return 1;
}
int search(const List *L, int x) {
    for (int i = 0; i < L->n; i++) if (L->a[i] == x) return i;
    return -1;
}
void show(const char *msg, const List *L) {
    printf("%-20s [", msg);
    for (int i = 0; i < L->n; i++) printf(i ? ", %d" : "%d", L->a[i]);
    printf("]  n=%d\n", L->n);
}

int main(void) {
    List L = {{10, 20, 30, 40}, 4};
    show("initial", &L);
    insert_at(&L, 2, 25);   show("insert 25 at 2", &L);
    delete_at(&L, 0);       show("delete position 0", &L);
    insert_at(&L, L.n, 99); show("append 99", &L);
    printf("search 30 -> index %d, search 77 -> index %d\n", search(&L, 30), search(&L, 77));
    printf("delete position 9 -> %s\n", delete_at(&L, 9) ? "done" : "invalid position");
    return 0;
}
```
```output
initial              [10, 20, 30, 40]  n=4
insert 25 at 2       [10, 20, 25, 30, 40]  n=5
delete position 0    [20, 25, 30, 40]  n=4
append 99            [20, 25, 30, 40, 99]  n=5
search 30 -> index 2, search 77 -> index -1
delete position 9 -> invalid position
```

## 4.4 Queue as a list

A queue is a list restricted to insertion at one end and deletion at the other. If it is stored as an array list with the front at index 0, enqueue is `insert_at(L, L->n, x)` (O(1)) and dequeue is `delete_at(L, 0)` (O(n), because everything shifts). Moving `front` instead of shifting gives the O(1) linear queue of Unit 3, and wrapping gives the circular queue. In a linked list, enqueue at the tail and dequeue at the head are both O(1) with a tail pointer (Unit 5). Likewise a stack is a list with insertion and deletion only at the end.

| Structure | Insert at | Delete at | Array-list cost |
|---|---|---|---|
| Stack | end | end | O(1) both |
| Queue | end (rear) | start (front) | O(1) + O(n) shifting, or O(1) with a moving front |
| General list | anywhere | anywhere | O(n) |

## Formula and fact sheet

- Array list: access O(1); insert/delete in the middle O(n) (shifting); search O(n), or O(log n) if sorted.
- Insert shifts from the **end** backwards; delete shifts from the **front** forwards.
- Linked list: access O(n); insert/delete after a known node O(1).
- Queue and stack are restricted lists.

## Chapter summary

- A list allows insertion, deletion and access at any position.
- Array lists are fast to index but slow to change in the middle; linked lists are the reverse.
- Shifting is the cost of contiguity; it explains why Unit 5's pointers are needed.
- Queues and stacks are lists with restricted access points.

## Practice

1. Define list ADT; name five operations.
2. Compare static and dynamic list structures in a table.
3. List [5, 9, 12, 20]. Show the list after insert(1, 7), then delete(3), then insert(4, 30).
4. How many element moves does inserting at position 0 cost in a list of n items? At the end?
5. Write the C code to delete the first occurrence of a value from an array list.
6. Why is dequeue from an array-list queue O(n) with the front fixed at index 0?
7. When would you prefer an array list to a linked list?

::: note Answers and worked solutions
**1.** An ordered collection allowing insert/delete at any position. Operations: insert, delete, get, set, search, traverse, length.
**2.** See the table in 4.2: array lists have O(1) access but O(n) middle insertion and fixed size; linked lists have O(n) access, O(1) insertion after a known node, and flexible size.
**3.** insert(1, 7): [5, 7, 9, 12, 20]. delete(3) removes 12: [5, 7, 9, 20]. insert(4, 30) appends: **[5, 7, 9, 20, 30]**.
**4.** Position 0: **n** moves. End: **0** moves.
**5.** `int p = search(L, x); if (p >= 0) delete_at(L, p);` using the functions above.
**6.** Removing index 0 requires moving each of the remaining n − 1 items one cell left.
**7.** When items are accessed by position or searched in sorted order (binary search), when the size is predictable, and when memory per item matters (no pointers).
:::
