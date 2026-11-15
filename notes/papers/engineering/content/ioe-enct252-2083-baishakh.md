---
file: NEBians-IOE-Past-Paper-Data-Structure-and-Algorithm-ENCT252-2083-Baishakh.pdf
subject: Data Structure and Algorithm
level: BE · Year II / Part II
code: ENCT 252
year_bs: 2083 Baishakh
cal: BS
year_ad: 2026
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
What does the Big-Omega notation determine in an algorithm analysis? Explain divide and conquer approach of an algorithm. [[3+2]]

@q 2
Define stack. Convert the following infix expression to postfix using stack. Infix expression: `A + B * (C ^ D - E) / (F - G + H)`. [[1+4]]

@q 3
Construct the recursive call tree for the Tower of Hanoi problem with 3 disks, showing each recursive call to move disks from peg A to peg C using peg B. [[3]]

@q 4
How circular queue overcomes the problem of linear queue in terms of memory efficiency? What do you mean by priority queue and what are their types? [[4+3]]

@q 5
Differentiate between static and dynamic list with suitable example. Write an algorithm to add two polynomials using linked list. [[3+4]]

@q 6
How do you delete a node with one child in binary search tree? Create a AVL tree for following sequence of elements: 3, 2, 1, 4, 5, 6, 7, 16, 15, 14, 13, 12. Construct a B-tree of order 3 for given data: 52, 46, 27, 81, 90, 108, 72, 110, 35, 115, 121, 86. [[1+4+4]]

@q 7
Define transitive closure. Explain Prim's algorithm with an example. Apply the Floyd-Warshall algorithm to find the shortest paths between all pairs of vertices in the following weighted directed graph: [[1+3+4]]

```figure caption="The weighted directed graph of Question 7: 1->3 (10), 3->1 (7), 1->2 (-3), 2->3 (6), 3->4 (3), 4->2 (2)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
E=[(1, 3, 10), (3, 1, 7), (1, 2, -3), (2, 3, 6), (3, 4, 3), (4, 2, 2)]
P={1:(0,2.2),3:(4,2.2),2:(0,0),4:(4,0)}
fig,ax=plt.subplots(figsize=(3.8,2.4)); ax.axis("off"); ax.set_aspect("equal"); ax.set_xlim(-1,5); ax.set_ylim(-0.9,3.3)
rads={(1,3):-0.3,(3,1):-0.3}
for u,v,w in E:
    rad=rads.get((u,v),0.0); a,b=P[u],P[v]
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle="-|>",color=ACCENT,lw=1.2,shrinkA=14,shrinkB=14,connectionstyle="arc3,rad=%s"%rad),zorder=2)
    dx,dy=b[0]-a[0],b[1]-a[1]; m=((a[0]+b[0])/2+0.5*rad*dy,(a[1]+b[1])/2-0.5*rad*dx)
    ax.text(m[0],m[1],str(w),ha="center",va="center",fontsize=8,color="#b00020",bbox=dict(fc="white",ec="none",pad=0.5),zorder=6)
for k,p in P.items():
    ax.add_patch(mp.Circle(p,0.36,fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(p[0],p[1],str(k),ha="center",va="center",fontsize=9,zorder=5)
```

@q 8
Define internal and external sorting. Sort the data 81, 89, 9, 11, 14, 76, 54, 22, 49 and 37 using Heap sort. Also define the time and space complexity of heap sort. [[2+5+1]]

@q 9
Explain sequential search efficiency. Write an algorithm for Binary search. Insert keys 89, 18, 49, 58 and 69 with hash table size 10 using quadratic probing. [[1+3+4]]

<!-- SOLUTIONS -->

@s 1
**Big-Omega notation** gives an **asymptotic lower bound** on the growth of a function (the running time of an algorithm). $f(n) = \Omega(g(n))$ means that there exist constants $c > 0$ and $n_0$ such that

$$\begin{gathered}f(n) \ge c \cdot g(n) \\ \text{for all } n \ge n_0\end{gathered}$$

So the algorithm needs **at least** about $g(n)$ steps for large inputs; $\Omega$ is used to state the best-case time or to prove that a problem cannot be solved faster than a given rate. Example: $f(n) = 3n^{2} + 2n$ is $\Omega(n^{2})$ because $3n^{2} + 2n \ge 3n^{2}$ for all $n \ge 1$ ($c = 3$, $n_0 = 1$). Compared with the other notations: $O$ is the upper bound ($f \le c\,g$), $\Omega$ the lower bound ($f \ge c\,g$) and $\Theta$ the tight bound (both). For linear search, best case $= \Omega(1)$ and worst case $= O(n)$.

**Divide and conquer.** The problem is solved recursively in three steps:

1. **Divide** the problem of size $n$ into $a$ smaller sub-problems of size about $n/b$ of the same kind.
2. **Conquer** each sub-problem recursively (a sub-problem small enough is solved directly, the base case).
3. **Combine** the sub-solutions into the solution of the original problem.

The running time is described by a recurrence $T(n) = a\,T(n/b) + f(n)$, where $f(n)$ is the cost of dividing and combining. By the master theorem merge sort ($a = 2$, $b = 2$, $f(n) = n$) gives $T(n) = 2T(n/2) + n = \Theta(n \log n)$.

```
MERGE-SORT(A, low, high)
  if low < high
      mid = (low + high) / 2
      MERGE-SORT(A, low, mid)          // conquer left half
      MERGE-SORT(A, mid + 1, high)     // conquer right half
      MERGE(A, low, mid, high)         // combine two sorted halves in O(n)
```

Other examples: quick sort, binary search ($T(n) = T(n/2) + 1$), Tower of Hanoi, Strassen's matrix multiplication.

@s 2
**Stack.** A stack is an ordered linear list in which insertion (**push**) and deletion (**pop**) take place at one end only, called the **top**. The last element inserted is the first one removed, so it is a **LIFO** (last in, first out) structure. Operations: push, pop, peek (read the top), isEmpty, isFull. Uses: function-call (recursion) stack, expression evaluation and conversion, undo, bracket matching, DFS.

**Infix to postfix using a stack.** Scan the infix expression from left to right:

1. operand: send it to the output;
2. `(`: push it;
3. `)`: pop operators to the output until `(` is popped (discard both brackets);
4. operator: pop from the stack to the output every operator of **higher or equal precedence** (left associative; `^` is right associative), then push the new operator;
5. at the end pop all remaining operators.

Precedence: `^` (highest), then `*` and `/`, then `+` and `-`.

| Symbol | Stack (bottom to top) | Postfix output | Action |
|---|---|---|---|
| `A` | ` ` | `A` | operand, send to output |
| `+` | `+` | `A` | push + |
| `B` | `+` | `AB` | operand, send to output |
| `*` | `+*` | `AB` | push * |
| `(` | `+*(` | `AB` | push ( |
| `C` | `+*(` | `ABC` | operand, send to output |
| `^` | `+*(^` | `ABC` | push ^ |
| `D` | `+*(^` | `ABCD` | operand, send to output |
| `-` | `+*(-` | `ABCD^` | pop ^ (higher or equal precedence), push - |
| `E` | `+*(-` | `ABCD^E` | operand, send to output |
| `)` | `+*` | `ABCD^E-` | pop to output until (: - |
| `/` | `+/` | `ABCD^E-*` | pop * (higher or equal precedence), push / |
| `(` | `+/(` | `ABCD^E-*` | push ( |
| `F` | `+/(` | `ABCD^E-*F` | operand, send to output |
| `-` | `+/(-` | `ABCD^E-*F` | push - |
| `G` | `+/(-` | `ABCD^E-*FG` | operand, send to output |
| `+` | `+/(+` | `ABCD^E-*FG-` | pop - (higher or equal precedence), push + |
| `H` | `+/(+` | `ABCD^E-*FG-H` | operand, send to output |
| `)` | `+/` | `ABCD^E-*FG-H+` | pop to output until (: + |
| `end` | ` ` | `ABCD^E-*FG-H+/+` | pop the remaining operators: / + |

$$\boxed{\,\text{Postfix} = A\,B\,C\,D\,\wedge\,E\,-\,*\,F\,G\,-\,H\,+\,/\,+\,}$$

(Check: the postfix string `ABCD^E-*FG-H+/+` was evaluated by computer for random values and always equals the infix value.)

@s 3
**Tower of Hanoi.** Move $n$ disks from peg A to peg C using peg B as helper, moving one disk at a time and never putting a larger disk on a smaller one. Recursive solution: move $n-1$ disks from the source to the auxiliary peg, move the largest disk to the destination, then move the $n-1$ disks from the auxiliary peg onto it.

```
HANOI(n, source, destination, auxiliary)
  if n == 1:  move disk 1 from source to destination;  return
  HANOI(n-1, source, auxiliary, destination)
  move disk n from source to destination
  HANOI(n-1, auxiliary, destination, source)
```

```figure caption="Recursive call tree of Tower of Hanoi for 3 disks, H(n, source, destination, auxiliary). Yellow boxes are the disk moves, numbered in the order they happen (left to right)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
def gtree(ax,T,dx=1.0,dy=1.0,w=0.9,fs=7):
    P={}; cnt=[0]
    def lay(t,d,path):
        lab,kind,ch=t
        if not ch: x=cnt[0]; cnt[0]+=1
        else:
            xs=[lay(c,d+1,path+(i,)) for i,c in enumerate(ch)]; x=(xs[0]+xs[-1])/2
        P[path]=(x*dx,-d*dy,lab,kind); return x
    lay(T,0,())
    for p,(x,y,lab,kind) in P.items():
        if p:
            px,py=P[p[:-1]][:2]; ax.plot([px,x],[py-0.2*dy,y+0.2*dy],color=INK,lw=0.9,zorder=1)
    for p,(x,y,lab,kind) in P.items():
        fc={"call":"white","base":"#eaf3ff","move":"#fff4d6"}[kind]
        box(ax,x,y,w,0.4*dy,lab,fc=fc,fs=fs)
    xs=[v[0] for v in P.values()]; ys=[v[1] for v in P.values()]
    ax.set_xlim(min(xs)-w,max(xs)+w); ax.set_ylim(min(ys)-0.5*dy,0.5*dy)
T=('H(3,A,C,B)', 'call', [('H(2,A,B,C)', 'call', [('move 1: disk 1\nA->C', 'move', []), ('move 2: disk 2\nA->B', 'move', []), ('move 3: disk 1\nC->B', 'move', [])]), ('move 4: disk 3\nA->C', 'move', []), ('H(2,B,C,A)', 'call', [('move 5: disk 1\nB->A', 'move', []), ('move 6: disk 2\nB->C', 'move', []), ('move 7: disk 1\nA->C', 'move', [])])])
fig,ax=plt.subplots(figsize=(7.6,3.4)); ax.axis("off")
gtree(ax,T,dx=1.0,dy=1.25,w=0.95,fs=6.2)
```

Reading the leaves from left to right gives the 7 moves ($2^{3} - 1$):

| Move | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| Disk | 1 | 2 | 1 | 3 | 1 | 2 | 1 |
| From to | A to C | A to B | C to B | A to C | B to A | B to C | A to C |

The tree has 3 calls with $n \ge 2$ and 4 calls with $n = 1$ (the leaves that make moves 1, 3, 5 and 7); in total there are 7 moves, and $T(n) = 2T(n-1) + 1$ gives $T(n) = 2^{n} - 1$ moves, i.e. exponential time $O(2^{n})$ and recursion depth $n$.

@s 4
**Problem of the linear queue.** In an array queue of size MAX, `rear` only moves forward. After MAX insertions `rear = MAX - 1` and the test `rear == MAX - 1` reports "queue full", even if many items were dequeued and the cells before `front` are empty. Those cells can never be used again, so memory is wasted (in the figure 4 of 8 cells are idle); the only cure for a linear queue is to shift all elements to the left, which costs $O(n)$ per operation.

**Solution: the circular queue.** Treat the array as a ring: the cell after index MAX-1 is index 0. `rear` and `front` advance as $(i + 1) \bmod \text{MAX}$, so freed cells are reused and the memory is used fully. The queue is full only when it really holds MAX items.

```figure caption="Left: a linear queue that is declared full although 4 cells are free. Right: a circular queue reuses those cells (rear wraps from 7 to 0)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
fig,(a1,a2)=plt.subplots(1,2,figsize=(7.0,2.8),gridspec_kw=dict(width_ratios=[1.25,1]))
a1.axis("off"); a1.set_xlim(-0.7,8.2); a1.set_ylim(-1.6,1.7)
items=["","","","","40","50","60","70"]
for i,t in enumerate(items):
    box(a1,i,0,0.85,0.7,t,fc="#fff4d6" if t else "white",fs=8); a1.text(i,-0.6,str(i),ha="center",fontsize=6.5,color="#555")
a1.text(4,0.85,"front",ha="center",fontsize=7,color=ACCENT); a1.text(7,0.85,"rear",ha="center",fontsize=7,color=ACCENT)
a1.set_title("Linear queue: rear = MAX-1, overflow",fontsize=7.5)
a2.axis("off"); a2.set_aspect("equal"); a2.set_xlim(-2.6,2.6); a2.set_ylim(-2.6,2.6)
vals={4:"40",5:"50",6:"60",7:"70",0:"80",1:"90"}
for i in range(8):
    th=_np.deg2rad(90-i*45); x,y=1.7*_np.cos(th),1.7*_np.sin(th)
    box(a2,x,y,0.7,0.5,vals.get(i,""),fc="#fff4d6" if i in vals else "white",fs=7.5)
    a2.text(2.25*_np.cos(th),2.25*_np.sin(th),str(i),ha="center",va="center",fontsize=6.5,color="#555")
a2.text(0,0.25,"front = 4",ha="center",fontsize=7,color=ACCENT); a2.text(0,-0.25,"rear = 1",ha="center",fontsize=7,color=ACCENT)
a2.set_title("Circular queue after 80, 90 are added",fontsize=7.5)
```

```
ENQUEUE(x)                               DEQUEUE()
1. if count == MAX: overflow, return     1. if count == 0: underflow, return
2. rear = (rear + 1) mod MAX             2. x = Q[front]
3. Q[rear] = x                           3. front = (front + 1) mod MAX
4. count = count + 1                     4. count = count - 1;  return x
```

(initially `front = 0`, `rear = -1`, `count = 0`; the counter distinguishes a full queue from an empty one, otherwise one cell is kept empty.) Both operations take $O(1)$ time.

```
#include <stdio.h>
#define MAX 5

int q[MAX], front = 0, rear = -1, count = 0;

void enqueue(int x) {
    if (count == MAX) { printf("enqueue %d: queue full\n", x); return; }
    rear = (rear + 1) % MAX;                       /* wrap around */
    q[rear] = x; count++;
}

int dequeue(void) {
    if (count == 0) { printf("queue empty\n"); return -1; }
    int x = q[front];
    front = (front + 1) % MAX;                     /* wrap around */
    count--;
    return x;
}

void show(void) {
    printf("front=%d rear=%d count=%d  items:", front, rear, count);
    for (int i = 0, k = front; i < count; i++, k = (k + 1) % MAX) printf(" %d", q[k]);
    printf("\n");
}

int main(void) {
    for (int x = 10; x <= 50; x += 10) enqueue(x);
    show();
    enqueue(60);
    printf("dequeue -> %d\n", dequeue());
    printf("dequeue -> %d\n", dequeue());
    enqueue(60); enqueue(70);                      /* these reuse the freed cells */
    show();
    return 0;
}
```

Output of the program (compiled with gcc and run):

```
front=0 rear=4 count=5  items: 10 20 30 40 50
enqueue 60: queue full
dequeue -> 10
dequeue -> 20
front=2 rear=1 count=5  items: 30 40 50 60 70
```

**Priority queue.** A priority queue is a queue in which every element has a **priority** and the element with the highest priority is served first, regardless of its arrival order; elements of equal priority are served in FIFO order. Typical use: CPU scheduling, Dijkstra's and Prim's algorithms, event simulation, Huffman coding.

**Types of priority queue:**

- **Ascending priority queue**: the element with the smallest key (priority number) is removed first (min-priority queue).
- **Descending priority queue**: the element with the largest key is removed first (max-priority queue).

(By implementation: an unordered list with $O(1)$ insert and $O(n)$ delete-min, an ordered list with $O(n)$ insert and $O(1)$ delete, or a binary heap with $O(\log n)$ for both.)

@s 5
**Static list and dynamic list.**

| Basis | Static list (array) | Dynamic list (linked list) |
|---|---|---|
| Size | fixed when it is declared | grows and shrinks at run time |
| Memory | contiguous block, allocated at compile time | nodes anywhere in memory, allocated with `malloc` at run time |
| Access | direct (random) access by index, $O(1)$ | sequential access from the head, $O(n)$ |
| Insertion / deletion | shifting of elements, $O(n)$ | change of pointers, $O(1)$ after the position is known |
| Memory use | wasted if not full, overflow if the size is too small | exactly one node per item, plus a pointer in each node |
| Example | `int marks[5] = {40, 50, 60, 70, 80};` | `10 -> 20 -> 30 -> NULL` with `struct node {int data; struct node *next;}` |

**Addition of two polynomials using linked lists.**

**Representation.** Each term $a_i x^{e_i}$ is stored in one node with three fields: the coefficient, the exponent and a pointer to the next term. The terms are kept in decreasing order of exponent, so two polynomials can be added in a single pass, like merging two sorted lists.

```figure caption="Polynomial 3x^4 + 2x^2 + 5x + 1 stored as a linked list: every node holds a coefficient, an exponent and the next pointer, in decreasing order of exponent."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
def cell(ax,x,y,w,h,t,fc="white",fs=8):
    ax.add_patch(mp.Rectangle((x,y-h/2),w,h,fc=fc,ec=INK,lw=1.2,zorder=3)); ax.text(x+w/2,y,t,ha="center",va="center",fontsize=fs,zorder=4)
fig,ax=plt.subplots(figsize=(6.4,1.5)); ax.axis("off"); ax.set_xlim(-0.3,12.6); ax.set_ylim(-1.1,1.1)
P=[(3,4),(2,2),(5,1),(1,0)]
ax.text(0.1,0,"head",fontsize=8,va="center",color=ACCENT); arr(ax,(0.75,0),(1.2,0))
for i,(c,e) in enumerate(P):
    x=1.2+i*2.9
    cell(ax,x,0,0.8,0.7,str(c),fc="#eaf3ff"); cell(ax,x+0.8,0,0.8,0.7,str(e),fc="#fff4d6"); cell(ax,x+1.6,0,0.6,0.7,"")
    ax.plot([x+1.9],[0],"o",color=ACCENT,ms=3.5,zorder=5)
    if i<len(P)-1: arr(ax,(x+1.9,0),(x+2.9,0))
    else: ax.text(x+2.45,0,"NULL",fontsize=7.5,va="center")
ax.text(1.6,0.62,"coef",fontsize=6.5,ha="center"); ax.text(2.4,0.62,"exp",fontsize=6.5,ha="center"); ax.text(3.1,0.62,"next",fontsize=6.5,ha="center")
```

**Algorithm ADD-POLY(P, Q)** (result in a new list R):

```
1.  p = head of P,  q = head of Q,  R = empty list
2.  while p != NULL and q != NULL
3.      if p.exp > q.exp:      append (p.coef, p.exp) to R;  p = p.next
4.      else if p.exp < q.exp: append (q.coef, q.exp) to R;  q = q.next
5.      else:                  s = p.coef + q.coef
6.                             if s != 0: append (s, p.exp) to R
7.                             p = p.next;  q = q.next
8.  while p != NULL: append (p.coef, p.exp) to R;  p = p.next
9.  while q != NULL: append (q.coef, q.exp) to R;  q = q.next
10. return R
```

The loop makes at most $m + n$ steps for polynomials with $m$ and $n$ terms, so the time is $O(m + n)$. **Example:** $P(x) = 3x^4 + 2x^2 + 5x + 1$ and $Q(x) = 4x^3 + 6x^2 + 2$. Step by step: exponent 4 only in $P$ gives $3x^4$; exponent 3 only in $Q$ gives $4x^3$; exponent 2 in both gives $2 + 6 = 8x^2$; exponent 1 only in $P$ gives $5x$; exponent 0 in both gives $1 + 2 = 3$. So $P + Q = 3x^4 + 4x^3 + 8x^2 + 5x + 3$. The following C program does exactly this:

```
#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int coef, exp; struct Node *next; } Node;

Node *append(Node *head, int c, int e) {          /* add a term at the end */
    Node *n = malloc(sizeof(Node));
    n->coef = c; n->exp = e; n->next = NULL;
    if (head == NULL) return n;
    Node *t = head;
    while (t->next != NULL) t = t->next;
    t->next = n;
    return head;
}

Node *add(Node *p, Node *q) {                      /* both lists sorted by decreasing exponent */
    Node *r = NULL;
    while (p != NULL && q != NULL) {
        if (p->exp > q->exp)      { r = append(r, p->coef, p->exp); p = p->next; }
        else if (p->exp < q->exp) { r = append(r, q->coef, q->exp); q = q->next; }
        else {                                     /* equal exponents: add the coefficients */
            int s = p->coef + q->coef;
            if (s != 0) r = append(r, s, p->exp);
            p = p->next; q = q->next;
        }
    }
    for (; p != NULL; p = p->next) r = append(r, p->coef, p->exp);   /* copy the leftover terms */
    for (; q != NULL; q = q->next) r = append(r, q->coef, q->exp);
    return r;
}

void show(const char *name, Node *h) {
    printf("%s = ", name);
    for (; h != NULL; h = h->next) printf("%+dx^%d ", h->coef, h->exp);
    printf("\n");
}

int main(void) {
    Node *p = NULL, *q = NULL;
    p = append(p, 3, 4); p = append(p, 2, 2); p = append(p, 5, 1); p = append(p, 1, 0);
    q = append(q, 4, 3); q = append(q, 6, 2); q = append(q, 2, 0);
    show("P(x)", p); show("Q(x)", q); show("P+Q ", add(p, q));
    return 0;
}
```

Output of the program (compiled with gcc and run):

```
P(x) = +3x^4 +2x^2 +5x^1 +1x^0 
Q(x) = +4x^3 +6x^2 +2x^0 
P+Q  = +3x^4 +4x^3 +8x^2 +5x^1 +3x^0
```

@s 6
**Deleting a node with one child from a binary search tree.** Let $x$ be the node to delete, having exactly one child $c$ (left or right).

```
DELETE-ONE-CHILD(x)
  1. find x and its parent p                (search the key as usual)
  2. c = x.left if x.left != NULL else x.right
  3. if x is the root:        root = c
     else if x == p.left:     p.left = c
     else:                    p.right = c
  4. free(x)
```

The only child (with its whole subtree) takes the place of the deleted node; the BST property still holds because every key in the subtree of $c$ lies on the same side of $p$ as $x$ did. For example, deleting 6 from the tree whose node 6 has only the right child 7 makes 7 the child of 6's parent. Time $O(h)$, where $h$ is the height of the tree. (Leaf: set the parent's link to NULL; two children: copy the in-order successor, then delete that node, which has at most one child.)

**AVL tree** (balance factor = height of left subtree minus height of right subtree, must stay in $\{-1, 0, +1\}$). Keys are inserted like in a BST, then the nodes on the path are checked; an imbalance is repaired by a single rotation (LL: right rotation, RR: left rotation) or a double rotation (LR, RL). Insertion sequence 3, 2, 1, 4, 5, 6, 7, 16, 15, 14, 13, 12; only the insertions that cause a rotation are listed (the others keep the tree balanced):

| Insert | Imbalance found at | Case | Rotation | 
|---|---|---|---|
| 1 | node 3 (balance factor +2) | LL | right rotation about 3 |
| 5 | node 3 (balance factor -2) | RR | left rotation about 3 |
| 6 | node 2 (balance factor -2) | RR | left rotation about 2 |
| 7 | node 5 (balance factor -2) | RR | left rotation about 5 |
| 15 | node 7 (balance factor -2) | RL | right rotation about 16, then left rotation about 7 |
| 14 | node 6 (balance factor -2) | RL | right rotation about 15, then left rotation about 6 |
| 13 | node 4 (balance factor -2) | RR | left rotation about 4 |
| 12 | node 14 (balance factor +2) | LL | right rotation about 14 |

```figure caption="AVL tree after inserting 3, 2, 1, 4, 5, 6, 7 (a perfect tree of height 3)."
import matplotlib.patches as mp
def bin_draw(ax,T,r=0.34,fs=8):
    out={}; cnt=[0]
    def go(n,d,par):
        if n is None: return
        go(n[1],d+1,n[0]); out[n[0]]=(cnt[0],d,par); cnt[0]+=1; go(n[2],d+1,n[0])
    go(T,0,None)
    for k,(x,d,par) in out.items():
        if par is not None:
            px,pd=out[par][0],out[par][1]; ax.plot([px,x],[-pd,-d],color=INK,lw=1,zorder=1)
    for k,(x,d,par) in out.items():
        ax.add_patch(mp.Circle((x,-d),r,fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(x,-d,str(k),ha="center",va="center",fontsize=fs,zorder=4)
    ax.set_xlim(-1,cnt[0]); ax.set_ylim(-max(v[1] for v in out.values())-0.8,0.8); ax.set_aspect("equal")
T=(4, (2, (1, None, None), (3, None, None)), (6, (5, None, None), (7, None, None)))
fig,ax=plt.subplots(figsize=(3.2,2.4)); ax.axis("off")
bin_draw(ax,T,fs=8)
```

```figure caption="Final AVL tree after also inserting 16, 15, 14, 13, 12 (height 4, every balance factor in -1, 0, +1)."
import matplotlib.patches as mp
def bin_draw(ax,T,r=0.34,fs=8):
    out={}; cnt=[0]
    def go(n,d,par):
        if n is None: return
        go(n[1],d+1,n[0]); out[n[0]]=(cnt[0],d,par); cnt[0]+=1; go(n[2],d+1,n[0])
    go(T,0,None)
    for k,(x,d,par) in out.items():
        if par is not None:
            px,pd=out[par][0],out[par][1]; ax.plot([px,x],[-pd,-d],color=INK,lw=1,zorder=1)
    for k,(x,d,par) in out.items():
        ax.add_patch(mp.Circle((x,-d),r,fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(x,-d,str(k),ha="center",va="center",fontsize=fs,zorder=4)
    ax.set_xlim(-1,cnt[0]); ax.set_ylim(-max(v[1] for v in out.values())-0.8,0.8); ax.set_aspect("equal")
T=(7, (4, (2, (1, None, None), (3, None, None)), (6, (5, None, None), None)), (15, (13, (12, None, None), (14, None, None)), (16, None, None)))
fig,ax=plt.subplots(figsize=(4.8,3.0)); ax.axis("off")
bin_draw(ax,T,fs=8)
```

Final AVL tree in text form (root 7): left subtree rooted at 4 with children 2 (1, 3) and 6 (left child 5); right subtree rooted at 15 with children 13 (12, 14) and 16. Its height is 4 and it was checked by computer to be a valid balanced search tree whose in-order list is 1, 2, ..., 7, 12, 13, ..., 16.

**B-tree of order 3** (each node holds at most 2 keys and 3 children, at least 1 key except the root; all leaves are on the same level). A key is inserted into the proper leaf; if a node then holds 3 keys, it is **split**: the middle key moves up to the parent and the other two keys form two nodes. Insertion of 52, 46, 27, 81, 90, 108, 72, 110, 35, 115, 121, 86:

| Insert | Splits caused | Tree after the insertion (a node is written [keys], its children follow in brackets) |
|---|---|---|
| 52 | none | `[52]` |
| 46 | none | `[46 52]` |
| 27 | node [27, 46, 52] overflows, median 46 moves up | `[46]([27], [52])` |
| 81 | none | `[46]([27], [52 81])` |
| 90 | node [52, 81, 90] overflows, median 81 moves up | `[46 81]([27], [52], [90])` |
| 108 | none | `[46 81]([27], [52], [90 108])` |
| 72 | none | `[46 81]([27], [52 72], [90 108])` |
| 110 | node [90, 108, 110] overflows, median 108 moves up; node [46, 81, 108] overflows, median 81 moves up | `[81]([46]([27], [52 72]), [108]([90], [110]))` |
| 35 | none | `[81]([46]([27 35], [52 72]), [108]([90], [110]))` |
| 115 | none | `[81]([46]([27 35], [52 72]), [108]([90], [110 115]))` |
| 121 | node [110, 115, 121] overflows, median 115 moves up | `[81]([46]([27 35], [52 72]), [108 115]([90], [110], [121]))` |
| 86 | none | `[81]([46]([27 35], [52 72]), [108 115]([86 90], [110], [121]))` |

```figure caption="Final B-tree of order 3 (at most 2 keys and 3 children per node; all leaves at the same level)."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
def mtree(ax,T,fs=8):
    P={}; cnt=[0.0]
    def lay(n,d,path):
        keys,ch=n; wdt=0.5*len(keys)+0.35
        if not ch: x=cnt[0]+wdt/2; cnt[0]+=wdt+0.35
        else:
            xs=[lay(c,d+1,path+(i,)) for i,c in enumerate(ch)]; x=(xs[0]+xs[-1])/2
        P[path]=(x,-d*1.4,keys,wdt); return x
    lay(T,0,())
    for p,(x,y,keys,wdt) in P.items():
        if p:
            px,py=P[p[:-1]][:2]; ax.plot([px,x],[py-0.22,y+0.22],color=INK,lw=1,zorder=1)
    for p,(x,y,keys,wdt) in P.items(): box(ax,x,y,wdt,0.44,"  ".join(map(str,keys)),fs=fs)
    xs=[v[0] for v in P.values()]; ys=[v[1] for v in P.values()]
    ax.set_xlim(min(xs)-1.2,max(xs)+1.2); ax.set_ylim(min(ys)-0.6,0.6)
T=([81], [([46], [([27, 35], []), ([52, 72], [])]), ([108, 115], [([86, 90], []), ([110], []), ([121], [])])])
fig,ax=plt.subplots(figsize=(6.8,2.6)); ax.axis("off")
mtree(ax,T,fs=8)
```

$$\boxed{\,\text{Root } [81];\ \text{children } [46] \text{ and } [108,\,115];\ \text{leaves } [27,35],\ [52,72],\ [86,90],\ [110],\ [121]\,}$$

@s 7
**Transitive closure.** The transitive closure of a relation $R$ on a set (equivalently of a directed graph $G$) is the smallest transitive relation $R^{+}$ containing $R$: there is an edge $(a, b)$ in $R^{+}$ exactly when $G$ has a **path of length at least 1** from $a$ to $b$. Warshall's algorithm computes it with $R^{(k)}[i][j] = R^{(k-1)}[i][j] \vee \big(R^{(k-1)}[i][k] \wedge R^{(k-1)}[k][j]\big)$ in $O(n^{3})$ time.

**Prim's algorithm** (minimum spanning tree of a connected weighted undirected graph). Start with any vertex; repeatedly add the cheapest edge that joins a vertex of the tree to a vertex outside it, until all vertices are included (a greedy algorithm; $O(E \log V)$ with a heap).

```
PRIM(G, start)
  T = {start};  tree edges = empty
  while T does not contain all vertices
      choose the minimum-weight edge (u, v) with u in T and v not in T
      add v to T and edge (u, v) to the tree
```

**Example.** Graph with vertices A to F and edges AB 4, AC 5, BC 11, BD 9, BE 7, CE 3, DE 13, DF 2, EF 6, started at A:

| Step | Tree vertices so far | Cheapest crossing edge | Weight |
|---|---|---|---|
| 1 | {A} | A-B | 4 |
| 2 | {A, B} | A-C | 5 |
| 3 | {A, B, C} | C-E | 3 |
| 4 | {A, B, C, E} | E-F | 6 |
| 5 | {A, B, C, E, F} | D-F | 2 |

Total weight $= 20$ with edges AB, AC, CE, EF, DF.

```figure caption="Minimum spanning tree (thick edges, total weight 20)."
E=[('A', 'B', 4), ('A', 'C', 5), ('B', 'D', 9), ('B', 'C', 11), ('B', 'E', 7), ('D', 'E', 13), ('D', 'F', 2), ('C', 'E', 3), ('E', 'F', 6)]
M=[('D', 'F'), ('C', 'E'), ('A', 'B'), ('A', 'C'), ('E', 'F')]
P={'A': (0, 1.2), 'B': (2.4, 2.6), 'D': (5.2, 2.6), 'C': (2.4, 0), 'E': (5.2, 0), 'F': (7.6, 1.2)}
fig,ax=plt.subplots(figsize=(5.0,2.4)); ax.axis("off"); ax.set_aspect("equal")
def inM(u,v): return (u,v) in M or (v,u) in M
for u,v,w in E:
    t=inM(u,v)
    ax.plot([P[u][0],P[v][0]],[P[u][1],P[v][1]],color=ACCENT if t else "#9aa",lw=3.0 if t else 1.1,zorder=1)
    mx,my=(P[u][0]+P[v][0])/2,(P[u][1]+P[v][1])/2
    ax.text(mx,my,str(w),fontsize=8,ha="center",va="center",bbox=dict(fc="white",ec="none",pad=0.6),zorder=4,color="#b00020" if t else INK)
for k,p in P.items(): ax.scatter([p[0]],[p[1]],s=330,color="white",edgecolor=INK,zorder=3); ax.text(p[0],p[1],k,ha="center",va="center",fontsize=9,zorder=5)
ax.set_xlim(-0.8, 8.5); ax.set_ylim(-0.8, 3.4)
```

**Floyd-Warshall algorithm.** For $k = 1 \dots n$ allow vertex $k$ as an intermediate vertex and update

$$d^{(k)}_{ij} = \min\big(d^{(k-1)}_{ij},\ d^{(k-1)}_{ik} + d^{(k-1)}_{kj}\big)$$

```
FLOYD-WARSHALL(W)            // W[i][j] = weight of edge i->j, 0 on the diagonal, infinity if no edge
  D = W
  for k = 1 to n
      for i = 1 to n
          for j = 1 to n
              if D[i][k] + D[k][j] < D[i][j]:  D[i][j] = D[i][k] + D[k][j]
  return D                   // O(n^3) time, O(n^2) space
```

Edges of the given graph: 1 to 3 (10), 3 to 1 (7), 1 to 2 (-3), 2 to 3 (6), 3 to 4 (3), 4 to 2 (2). There is no negative cycle (the cycles 1-2-3-1 and 2-3-4-2 have weights 10 and 11).

**Initial matrix $D^{(0)}$ (direct edges)**

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 0 | -3 | 10 | ∞ |
| **2** | ∞ | 0 | 6 | ∞ |
| **3** | 7 | ∞ | 0 | 3 |
| **4** | ∞ | 2 | ∞ | 0 |

**$D^{(1)}$: paths allowed to pass through vertices 1 to 1**

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 0 | -3 | 10 | ∞ |
| **2** | ∞ | 0 | 6 | ∞ |
| **3** | 7 | 4 | 0 | 3 |
| **4** | ∞ | 2 | ∞ | 0 |

**$D^{(2)}$: paths allowed to pass through vertices 1 to 2**

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 0 | -3 | 3 | ∞ |
| **2** | ∞ | 0 | 6 | ∞ |
| **3** | 7 | 4 | 0 | 3 |
| **4** | ∞ | 2 | 8 | 0 |

**$D^{(3)}$: paths allowed to pass through vertices 1 to 3**

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 0 | -3 | 3 | 6 |
| **2** | 13 | 0 | 6 | 9 |
| **3** | 7 | 4 | 0 | 3 |
| **4** | 15 | 2 | 8 | 0 |

**$D^{(4)}$: paths allowed to pass through vertices 1 to 4**

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 0 | -3 | 3 | 6 |
| **2** | 13 | 0 | 6 | 9 |
| **3** | 7 | 4 | 0 | 3 |
| **4** | 15 | 2 | 8 | 0 |


**Reading the final matrix $D^{(4)}$** (shortest distances, row = from, column = to), for example $d(1,3) = 3$ by the path $1 \to 2 \to 3$ ($-3 + 6$, shorter than the direct edge 10), $d(1,4) = 6$ by $1 \to 2 \to 3 \to 4$, $d(2,1) = 13$ by $2 \to 3 \to 1$, $d(4,1) = 15$ by $4 \to 2 \to 3 \to 1$ and $d(4,3) = 8$ by $4 \to 2 \to 3$.

$$\boxed{\,D^{(4)} = \begin{pmatrix} 0 & -3 & 3 & 6 \\ 13 & 0 & 6 & 9 \\ 7 & 4 & 0 & 3 \\ 15 & 2 & 8 & 0 \end{pmatrix}\,}$$

(The result was verified by running the algorithm in code.) The closure of the same graph, by Warshall's rule, is the matrix of all 1s, because every vertex can reach every other vertex (the graph is strongly connected):

**Reachability (Warshall) matrix $R^{(4)}$**

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| **1** | 1 | 1 | 1 | 1 |
| **2** | 1 | 1 | 1 | 1 |
| **3** | 1 | 1 | 1 | 1 |
| **4** | 1 | 1 | 1 | 1 |


@s 8
**Internal sorting** sorts data that fits entirely in the main memory (RAM) of the computer, e.g. bubble, insertion, selection, quick, heap sort. **External sorting** is used when the data is too big for memory and lives on disk or tape: chunks are sorted in memory and written as runs, then the runs are merged (external merge sort).

**Heap sort** (ascending order, max-heap). Phase 1: build a max-heap (every parent is at least as large as its children) from the array by heapifying from the last parent $\lfloor n/2 \rfloor$ down to the root. Phase 2: repeatedly swap the root (the maximum) with the last element of the heap, shrink the heap by one and sift the new root down.

```
HEAPSORT(A, n)
  for i = n/2 downto 1:  HEAPIFY(A, i, n)          // build max-heap, O(n)
  for last = n downto 2:
      swap A[1] and A[last]                        // largest goes to its final place
      HEAPIFY(A, 1, last - 1)                      // restore the heap, O(log n)
```

Array (index 1 to 10): 81, 89, 9, 11, 14, 76, 54, 22, 49, 37.

```figure caption="The given data as a complete binary tree (node numbers in red)."
import matplotlib.patches as mp
A=[81, 89, 9, 11, 14, 76, 54, 22, 49, 37]
fig,ax=plt.subplots(figsize=(4.6,2.6)); ax.axis("off")
import math
n=len(A); L=int(math.log2(n))+1
P={}
for i in range(n):
    lv=int(math.log2(i+1)); j=i-(2**lv-1); P[i]=((j+0.5)/2**lv*8,-lv*1.1)
for i in range(1,n):
    p=(i-1)//2; ax.plot([P[p][0],P[i][0]],[P[p][1],P[i][1]],color=INK,lw=1,zorder=1)
for i in range(n):
    ax.add_patch(mp.Circle(P[i],0.34,fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(P[i][0],P[i][1],str(A[i]),ha="center",va="center",fontsize=8,zorder=4); ax.text(P[i][0]+0.42,P[i][1]+0.34,str(i+1),fontsize=6,color="#b00020")
ax.set_xlim(-0.8,8.8); ax.set_ylim(-(L-1)*1.1-0.7,0.7); ax.set_aspect("equal")
```

```figure caption="The max-heap built by bottom-up heapify (largest key 89 at the root)."
import matplotlib.patches as mp
A=[89, 81, 76, 49, 37, 9, 54, 22, 11, 14]
fig,ax=plt.subplots(figsize=(4.6,2.6)); ax.axis("off")
import math
n=len(A); L=int(math.log2(n))+1
P={}
for i in range(n):
    lv=int(math.log2(i+1)); j=i-(2**lv-1); P[i]=((j+0.5)/2**lv*8,-lv*1.1)
for i in range(1,n):
    p=(i-1)//2; ax.plot([P[p][0],P[i][0]],[P[p][1],P[i][1]],color=INK,lw=1,zorder=1)
for i in range(n):
    ax.add_patch(mp.Circle(P[i],0.34,fc="white",ec=INK,lw=1.2,zorder=3)); ax.text(P[i][0],P[i][1],str(A[i]),ha="center",va="center",fontsize=8,zorder=4); ax.text(P[i][0]+0.42,P[i][1]+0.34,str(i+1),fontsize=6,color="#b00020")
ax.set_xlim(-0.8,8.8); ax.set_ylim(-(L-1)*1.1-0.7,0.7); ax.set_aspect("equal")
```

| Step | Array (heap part, then sorted part after the bar) |
|---|---|
| heapify node 5 | 81, 89, 9, 11, 37, 76, 54, 22, 49, 14 |
| heapify node 4 | 81, 89, 9, 49, 37, 76, 54, 22, 11, 14 |
| heapify node 3 | 81, 89, 76, 49, 37, 9, 54, 22, 11, 14 |
| heapify node 2 | 81, 89, 76, 49, 37, 9, 54, 22, 11, 14 |
| heapify node 1 | 89, 81, 76, 49, 37, 9, 54, 22, 11, 14 |
| extract 89: swap with last, shrink, sift down | 81, 49, 76, 22, 37, 9, 54, 14, 11 \| **89** |
| extract 81: swap with last, shrink, sift down | 76, 49, 54, 22, 37, 9, 11, 14 \| **81, 89** |
| extract 76: swap with last, shrink, sift down | 54, 49, 14, 22, 37, 9, 11 \| **76, 81, 89** |
| extract 54: swap with last, shrink, sift down | 49, 37, 14, 22, 11, 9 \| **54, 76, 81, 89** |
| extract 49: swap with last, shrink, sift down | 37, 22, 14, 9, 11 \| **49, 54, 76, 81, 89** |
| extract 37: swap with last, shrink, sift down | 22, 11, 14, 9 \| **37, 49, 54, 76, 81, 89** |
| extract 22: swap with last, shrink, sift down | 14, 11, 9 \| **22, 37, 49, 54, 76, 81, 89** |
| extract 14: swap with last, shrink, sift down | 11, 9 \| **14, 22, 37, 49, 54, 76, 81, 89** |
| extract 11: swap with last, shrink, sift down | 9 \| **11, 14, 22, 37, 49, 54, 76, 81, 89** |

$$\boxed{\,\text{Sorted: } 9,\ 11,\ 14,\ 22,\ 37,\ 49,\ 54,\ 76,\ 81,\ 89\,}$$

**Complexity of heap sort.** Building the heap costs $O(n)$ and each of the $n - 1$ extractions costs $O(\log n)$, so the time is $O(n \log n)$ in the best, average and worst case. The space complexity is $O(1)$ extra space, because the sort is done in place on the array (it is not stable).

@s 9
**Efficiency of sequential (linear) search.** The key is compared with the elements one by one from the first element.

| Case | Comparisons | Order |
|---|---|---|
| Best (key is the first element) | 1 | $O(1)$ |
| Average (key equally likely at any position) | $(n + 1)/2$ | $O(n)$ |
| Worst (key is last or absent) | $n$ | $O(n)$ |

It works on unsorted data and needs no extra memory, but it is slow for large $n$; the space complexity is $O(1)$.

**Binary search algorithm** (on a list sorted in ascending order): compare the key with the middle element; if equal stop, if smaller continue in the left half, otherwise in the right half.

```
BINARY-SEARCH(A, n, key)
  low = 0;  high = n - 1
  while low <= high
      mid = (low + high) / 2
      if A[mid] == key:  return mid
      else if key < A[mid]:  high = mid - 1
      else:                  low = mid + 1
  return -1                       // not found
```

The search space halves each time, so $T(n) = T(n/2) + 1$ gives $O(\log n)$ in the worst case ($O(1)$ best case). A C implementation with a trace:

```
#include <stdio.h>

int binary_search(int a[], int n, int key) {       /* a[] sorted in ascending order */
    int low = 0, high = n - 1;
    while (low <= high) {
        int mid = (low + high) / 2;
        printf("  low=%d high=%d mid=%d a[mid]=%d\n", low, high, mid, a[mid]);
        if (a[mid] == key) return mid;             /* found */
        else if (key < a[mid]) high = mid - 1;     /* continue in the left half */
        else low = mid + 1;                        /* continue in the right half */
    }
    return -1;                                     /* not found */
}

int main(void) {
    int a[] = {10, 20, 30, 35, 40, 50, 80, 90};
    int n = sizeof a / sizeof a[0];
    printf("search 35:\n"); printf("index = %d\n", binary_search(a, n, 35));
    printf("search 55:\n"); printf("index = %d\n", binary_search(a, n, 55));
    return 0;
}
```

Output of the program (compiled with gcc and run):

```
search 35:
  low=0 high=7 mid=3 a[mid]=35
index = 3
search 55:
  low=0 high=7 mid=3 a[mid]=35
  low=4 high=7 mid=5 a[mid]=50
  low=6 high=7 mid=6 a[mid]=80
index = -1
```

**Quadratic probing.** Hash function $h(k) = k \bmod 10$. If cell $h(k)$ is occupied, try $(h(k) + i^{2}) \bmod 10$ for $i = 1, 2, 3, \dots$ (offsets 1, 4, 9, ...).

| Key | h(k) = k mod 10 | Probe positions tried ((h + i squared) mod 10) | Stored at |
|---|---|---|---|
| 89 | 9 | 9 | **9** |
| 18 | 8 | 8 | **8** |
| 49 | 9 | 9, 0 | **0** |
| 58 | 8 | 8, 9, 2 | **2** |
| 69 | 9 | 9, 0, 3 | **3** |

Hash table after all insertions:

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Key | 49 | - | 58 | 69 | - | - | - | - | 18 | 89 |

$$\boxed{\,\text{Table: } 0 \to 49,\ 2 \to 58,\ 3 \to 69,\ 8 \to 18,\ 9 \to 89\,}$$

Quadratic probing avoids the long clusters (primary clustering) of linear probing, but keys with the same home cell follow the same probe sequence (secondary clustering).
