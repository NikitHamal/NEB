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

## 4.5 Seeing the ideas: the list as an ordered collection

A list is a collection in which the order matters and every item has a position. A library card catalogue is a very good picture of one: the cards stand in a fixed order, a new card must be slipped into the right place and every card behind it moves one step. That is exactly what happens to the items of an array-based list, as the plate and the figures show.

```photogrid label="4.1" cols="2" ratio="1.1" caption="A list needs order and positions. (a) A card catalogue drawer: the cards are kept in alphabetical order, so adding a card in the middle means pushing all later cards back by one place. (b) The same operation in an array-based list: to insert 25 at position 2 in the list 10, 20, 30, 40, the items 40 and 30 shift one cell to the right, from the end backwards, and then 25 is placed. Two shifts were needed because two items stood at or after position 2."
@ photo id="bca202/catalog" cap="Cards in a catalogue form an ordered list"
fit 1.1
focus 0.5 0.5
@ svg cap="Insert 25 at position 2 in an array list"
f = Fig(300, 240)
f.text(150, 14, "before: n = 4", size=10.5, color=NAVY, bold=True)
for i, v in enumerate(["10", "20", "30", "40", ""]):
    f.box(20 + i * 52, 24, 48, 34, v, fill=BLUE if v else SOFT, stroke=NAVY, size=12, bold=True, r=0, dash=(not v))
    f.text(44 + i * 52, 72, "[%d]" % i, size=9.5, color=SLATE)
f.arrow([(176, 110), (228, 110)], color=RED, sw=1.6); f.arrow([(124, 110), (176, 110)], color=RED, sw=1.6)
f.text(150, 98, "shift 40, then 30", size=9.5, color=RED, bold=True)
f.text(150, 140, "after: n = 5", size=10.5, color=NAVY, bold=True)
for i, v in enumerate(["10", "20", "25", "30", "40"]):
    f.box(20 + i * 52, 150, 48, 34, v, fill=SAND if v == "25" else MINT, stroke=AMBER if v == "25" else TEAL, size=12, bold=True, r=0)
    f.text(44 + i * 52, 198, "[%d]" % i, size=9.5, color=SLATE)
f.text(150, 224, "work = n - pos = 4 - 2 = 2 shifts", size=10, color=TEAL, bold=True)
```

```svgfig label="4.1" caption="The cost of inserting into an array list of n = 6 items depends on the position. Inserting at position p needs n - p shifts, so it needs 6 shifts at the front (position 0), 3 in the middle (position 3) and 0 at the end (position 6). The average over the seven possible positions is (6 + 5 + 4 + 3 + 2 + 1 + 0) / 7 = 3 shifts, which is n / 2. Deletion from position p needs n - p - 1 shifts. Both are therefore O(n) in the worst case, while reading an item by position is O(1)."
f = Fig(580, 200)
f.text(290, 14, "shifts needed to insert into a list of n = 6 items, by position", size=10.5, color=NAVY, bold=True)
for p in range(7):
    s = 6 - p
    x = 20 + p * 78
    h = s * 20
    f.box(x, 170 - h, 56, max(h, 3), "", fill=SAND if s else MINT, stroke=AMBER if s else TEAL, r=0)
    f.text(x + 28, 162 - h if h else 160, str(s), size=11, color=AMBER if s else TEAL, bold=True)
    f.text(x + 28, 184, "pos %d" % p, size=9.5, color=SLATE)
f.text(450, 40, "average = 3 = n / 2", size=10.5, color=RED, bold=True)
```

```svgfig label="4.2" caption="Static and dynamic implementations of the List ADT side by side. A static (array) list stores items in consecutive cells, gives direct access by index, and must be given a maximum size in advance, so unused cells are wasted and a full array cannot grow. A dynamic (linked) list stores each item in a separate node that holds the address of the next node, so it grows one node at a time and insertion needs no shifting, but reaching the i-th item needs i steps."
f = Fig(580, 200)
f.text(145, 14, "Static list (array)", size=11, color=NAVY, bold=True)
for i, v in enumerate(["A", "B", "C", "", ""]):
    f.box(10 + i * 56, 30, 52, 36, v, fill=BLUE if v else SOFT, stroke=NAVY, size=12, bold=True, r=0, dash=(not v))
f.text(145, 88, "index access O(1); fixed size; wasted cells", size=9.5, color=SLATE)
f.text(145, 106, "insert/delete: shifting, O(n)", size=9.5, color=RED, bold=True)
f.text(435, 14, "Dynamic list (linked)", size=11, color=TEAL, bold=True)
for i, v in enumerate(["A", "B", "C"]):
    x = 320 + i * 86
    f.box(x, 30, 56, 36, v, fill=MINT, stroke=TEAL, size=12, bold=True)
    f.box(x + 56, 30, 18, 36, "", fill=SAND, stroke=AMBER, r=0)
    if i < 2: f.arrow([(x + 65, 48), (x + 86, 48)], color=AMBER, sw=1.5)
f.text(435, 88, "i-th item needs i steps; grows as needed", size=9.5, color=SLATE)
f.text(435, 106, "insert/delete: change pointers, O(1)", size=9.5, color=TEAL, bold=True)
f.box(10, 135, 560, 50, "Choose an array when the size is known and reads dominate; choose a linked list when the size changes and\ninsertions or deletions dominate (details in Unit 5).", fill=SOFT, stroke=SLATE, size=10, bold=True)
```

Two ways to build the same list differ most when something is inserted in the middle. A railway train is the natural picture of the linked version: each coach is a node and the coupling is a pointer.

```photogrid label="4.2" cols="2" ratio="1.2" caption="Array list or linked list? (a) A Nepal Railways train at Janakpur: each coach is coupled to the next, so a coach can be added anywhere by changing couplings, with no need to move the other coaches. An array list is more like seats bolted to a floor: to add one in the middle every later seat must shift along. (b) For a list of n = 8 items, inserting at position k costs n - k shifts in an array, but about k pointer steps (nodes visited) in a linked list. The array is best at the end, the linked list at the front. Both counts are produced by simulation and asserted."
@ photo id="bca203/janakpur" cap="Nepal Railways train, Janakpur station"
fit 1.2
focus 0.5 0.5
@ svg cap="Cost of inserting at position k, n = 8"
n = 8
def arr_cost(k):
    a = list(range(n)); moves = 0
    a.append(None)
    for j in range(n, k, -1): a[j] = a[j - 1]; moves += 1
    a[k] = "new"; return moves
def ll_cost(k):
    nxt = {i: i + 1 for i in range(n)}; nxt[n - 1] = None
    cur = -1; steps = 0
    for _ in range(k): cur = cur + 1 if cur >= 0 else 0; steps += 1
    return steps
rows = [(k, arr_cost(k), ll_cost(k)) for k in range(n + 1)]
assert all(a == n - k and l == k for k, a, l in rows) and rows[0][1] == 8 and rows[8][2] == 8
f = Fig(300, 268)
f.text(150, 11, "operations to insert at position k", size=10, color=NAVY, bold=True)
f.box(70, 20, 12, 9, "", fill=RED, stroke=RED, r=0); f.text(86, 25, "array: shifts", size=9, color=RED, bold=True, anchor="start")
f.box(170, 20, 12, 9, "", fill=TEAL, stroke=TEAL, r=0); f.text(186, 25, "linked: steps", size=9, color=TEAL, bold=True, anchor="start")
for i, (k, a, l) in enumerate(rows):
    y = 36 + i * 22
    f.text(10, y + 11, "k = %d" % k, size=9.5, color=SLATE, bold=True, anchor="start")
    f.box(50, y, max(a * 28, 1), 9, "", fill=RED, stroke=RED, r=0)
    f.text(50 + a * 28 + 4, y + 8, str(a), size=9, color=RED, bold=True, anchor="start")
    f.box(50, y + 10, max(l * 28, 1), 9, "", fill=TEAL, stroke=TEAL, r=0)
    f.text(50 + l * 28 + 4, y + 18, str(l), size=9, color=TEAL, bold=True, anchor="start")
f.text(150, 258, "total over all positions: array %d, linked %d" % (sum(r[1] for r in rows), sum(r[2] for r in rows)), size=9.5, color=NAVY, bold=True)
```

### 4.5.1 Eight applications of lists

1. **Student and result lists.** A class roll list, a merit list of an entrance examination and the result sheet of TU are lists in which the order and the position carry meaning. The program reads the item at a given rank directly. An array list suits these because the number of students is known.
2. **Playlists and queues of songs.** A music player keeps songs in a list. The user can insert a song after the current one, delete another and move to the next one. The position of a song decides when it plays.
3. **Shopping carts and billing.** A cart of an online shop is a list of products with prices. Adding or removing an item changes the list, and the bill is the sum over the list. The order of items on the bill is the order in which they were added.
4. **Text editors.** A document is a list of lines or characters. Typing inserts a character in the middle and deleting removes one. Editors use special list structures so that these operations do not shift the whole file.
5. **Polynomials and sparse data.** A polynomial such as 3x squared plus 5x plus 7 is stored as a list of coefficients. Adding two polynomials is done by walking along both lists. Only the non-zero terms need to be stored in a linked version.
6. **Implementing other structures.** Stacks, queues and deques are special lists with restricted insertion and deletion. Their array and linked implementations reuse list operations. The list is therefore the base of many other ADTs.
7. **Timetables and schedules.** A college routine is an ordered list of periods. Inserting a period shifts later periods in time. Searching by position (period 3) is direct.
8. **Records of transactions.** A mini-statement of a bank account or of the Fonepay wallet is a list of transactions in time order. New records are appended at the end, and the list is read from the end towards the beginning. Appending to an array list is O(1) when space is available.

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

## Model answers (5 and 10 marks)

**Q1. Define the List ADT and list its operations. (5 marks)**

A **list** is a finite, ordered collection of items of the same type in which every item has a position and, except for the first and last, one predecessor and one successor. The **List ADT** specifies the data and operations without telling how the items are stored (Plate 4.1).

**Operations**
1. `create()` or `init()`: make an empty list.
2. `insert(x, pos)`: put x at position pos; later items move one place on.
3. `delete(pos)`: remove the item at pos; later items close the gap.
4. `get(pos)`: return the item at pos.
5. `search(x)`: return the position of x, or -1 if absent.
6. `length()`, `isEmpty()`, `isFull()`: report the state.
7. `traverse()`: visit every item in order.

**Rules.** A position must lie between 0 and the current length for insertion and between 0 and length - 1 for deletion and reading; otherwise the operation is an error. Duplicates are allowed unless the specification forbids them. The ADT can be implemented statically with an array or dynamically with a linked list. For example, inserting 25 at position 2 in the list 10, 20, 30, 40 gives 10, 20, 25, 30, 40.

**Q2. Differentiate between static (array) and dynamic (linked) implementations of a list. (5 marks)**

In a **static implementation** the items are kept in consecutive cells of an array whose maximum size is declared in advance. In a **dynamic implementation** each item is stored in a separate node obtained at run time (`malloc`) that also holds the address of the next node (Figure 4.2).

| Point | Array (static) | Linked (dynamic) |
|---|---|---|
| Size | fixed at compile time | grows and shrinks at run time |
| Memory | unused cells are wasted; overflow when full | exactly one node per item plus the pointer |
| Access by position | O(1) | O(n) |
| Insert / delete in the middle | O(n) because of shifting | O(1) once the node is found |
| Extra space per item | none | one pointer |
| Cache behaviour | good (contiguous) | poorer (scattered) |

An array list is preferred when the size is known and reading by index is frequent, for example a roll list of 40 students. A linked list is preferred when the size varies and insertions are frequent, for example a playlist. The choice is a trade-off between speed of access and flexibility of size, and it is the reason why both implementations are taught.

**Q3. Explain the array implementation of a list with insertion and deletion algorithms, and discuss their time complexity. (10 marks)**

**Introduction.** In the array implementation the list is stored in `int a[MAX]` and an integer `n` holds the current number of items. The item at position i is `a[i]`, which makes access by position immediate. The price is paid in insertion and deletion, which must move items to keep them consecutive.

**Insertion algorithm, `insert(x, pos)`.**
1. If `n == MAX`, report overflow and stop.
2. If `pos < 0` or `pos > n`, report an invalid position and stop.
3. For `i` from `n - 1` down to `pos`, set `a[i + 1] = a[i]`. (The loop runs backwards so that no item is overwritten.)
4. Set `a[pos] = x`.
5. Set `n = n + 1`.

**Deletion algorithm, `delete(pos)`.**
1. If `pos < 0` or `pos >= n`, report an invalid position and stop.
2. Save `x = a[pos]`.
3. For `i` from `pos` to `n - 2`, set `a[i] = a[i + 1]`. (The loop runs forwards.)
4. Set `n = n - 1` and return x.

**Worked example (Plate 4.1b).** Start with 10, 20, 30, 40 and `n = 4`. `insert(25, 2)` shifts 40 to `a[4]` and 30 to `a[3]` (two shifts, which equals `n - pos = 4 - 2`), places 25 in `a[2]` and makes `n = 5`. Now `delete(0)` removes 10 and moves 20, 25, 30, 40 one place left (four shifts, equal to `n - pos - 1 = 5 - 0 - 1`), leaving 20, 25, 30, 40.

**Complexity.** Insertion needs `n - pos` shifts and deletion `n - pos - 1`. Figure 4.1 shows that for `n = 6` the work is 6 at the front, 3 in the middle and 0 at the end, with an average of `n / 2`.

| Operation | Best case | Worst case | Average |
|---|---|---|---|
| Access `a[i]` | O(1) | O(1) | O(1) |
| Insert | O(1) at the end | O(n) at the front | O(n) |
| Delete | O(1) at the end | O(n) at the front | O(n) |
| Search (unsorted) | O(1) | O(n) | O(n) |
| Space | O(MAX) | O(MAX) | O(MAX) |

**Conclusion.** The array list is simple and gives constant-time access, but its fixed capacity and the O(n) shifting make it a poor choice for lists that change often. These weaknesses lead to the linked list of Unit 5.
