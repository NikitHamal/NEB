---
file: NEBians-IOE-Past-Paper-Data-Structure-and-Algorithm-ENCT252-2082-Bhadra.pdf
subject: Data Structure and Algorithm
level: BE · Year II / Part II
code: ENCT 252
year_bs: 2082 Bhadra
cal: BS
year_ad: 2025
stream: BCT
time: 3 hrs
marks: 60
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular (New Course). Pass marks 24.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Define data structure. Differentiate between linear and non-linear data structures with examples. What is the rate of growth of an algorithm, and why is it important? [[1+2+2]]

@q 2
Convert following infix expression into postfix expression showing status of stack in each step `A*B - (C*D - (E/F) $ G*H) - I`. Generate a recursion tree to evaluate 4th Fibonacci term. [[4+4]]

@q 3
What is the problem with linear queue implementation? Also explain solution for the problem with example and respective enqueue and dequeue algorithms. [[2+2+3]]

@q 4
In a linked list data cannot be accessed randomly, justify with suitable example. Explain with algorithm how the addition of polynomial equations is done using linked list. [[2+5]]

@q 5
a) Define a linked list. Write algorithms for push and pop operations in the dynamic implementation of a stack using a singly linked list. [[1+3]]

b) Write an algorithm to insert a node at a specified position in a doubly linked list. Describe how a polynomial can be represented using a linked list with an example. [[3+2]]

@q 6
Define minimum spanning tree. Write an algorithm to find MST using Kruskal's algorithm. Find the shortest path from point A to point F using Dijkstra's algorithm. [[1+3+4]]

```figure caption="The graph of Question 6."
E=[('A', 'B', 4), ('A', 'C', 5), ('B', 'D', 9), ('B', 'C', 11), ('B', 'E', 7), ('D', 'E', 13), ('D', 'F', 2), ('C', 'E', 3), ('E', 'F', 6)]
M=[]
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

@q 7
What do you mean by in place and not in place sorting? Explain. Sort the given elements using quick sort algorithm, showing important steps: 20, 50, 40, 30, 10, 90, 80, 35. [[3+5]]

@q 8
Define hashing. Write an algorithm for binary search. Insert keys 12, 22, 34, 41, 53, 64, 79 into a hash table of size 10 using linear probing with hash function $h(k) = k \bmod 10$. Show each step and the final table. [[1+3+4]]

<!-- SOLUTIONS -->

@s 1
**Data structure.** A data structure is a particular way of organising, storing and relating data in the memory of a computer so that it can be accessed and modified efficiently (together with the operations defined on it). Examples: array, stack, queue, linked list, tree, graph, hash table.

**Linear and non-linear data structures.**

| Basis | Linear data structure | Non-linear data structure |
|---|---|---|
| Arrangement | elements form a sequence; each element has one predecessor and one successor (except the ends) | an element can be connected to several others (hierarchy or network) |
| Traversal | single run, one level | cannot be traversed in one pass in a straight line; needs BFS/DFS or tree traversals |
| Memory use | simple, contiguous (array) or linked | usually linked, harder to implement |
| Examples | array, linked list, stack, queue | tree, binary search tree, heap, graph |

**Rate of growth of an algorithm.** The rate of growth (order of growth) describes how the running time (or memory) of an algorithm increases as the input size $n$ increases; only the dominant term matters for large $n$, so $3n^{2} + 5n + 7$ grows like $n^{2}$. It is written with the asymptotic notations $O$, $\Omega$, $\Theta$. It is important because

- it compares algorithms independently of the machine, language and compiler;
- it predicts whether an algorithm stays usable when the input becomes large (an $O(n^{2})$ method that is fine for 100 items may be hopeless for a million);
- it guides the choice of the algorithm and data structure (for example linear search $O(n)$ against binary search $O(\log n)$).

| Growth rate | n = 10 | n = 100 | n = 1000 |
|---|---|---|---|
| 1 | 1 | 1 | 1 |
| log2 n | 3 | 7 | 10 |
| n | 10 | 100 | 1000 |
| n log2 n | 33 | 664 | 9966 |
| n squared | 100 | 10000 | 1000000 |
| 2 to the n | 1024 | 1.3e+30 | 1.1e+301 |

(Values are the number of basic steps; $2^{n}$ for $n = 100$ and $n = 1000$ is astronomically large, which is why exponential algorithms are impractical.) The usual order is $1 < \log n < n < n \log n < n^{2} < n^{3} < 2^{n} < n!$.

@s 2
**Reading the expression.** The operator `$` means exponentiation (highest precedence, right associative, written `^` in other papers), then come `*` and `/`, then `+` and `-`. So `$` binds tighter than `*`: the expression is `A*B - (C*D - ((E/F) $ G) * H) - I`. Rules: operands go straight to the output; `(` is pushed; `)` pops to the output until `(`; an operator pops every operator of higher or equal precedence (for `$`, only strictly higher) and is pushed; at the end everything left is popped.

| Symbol | Stack (bottom to top) | Postfix output | Action |
|---|---|---|---|
| `A` | ` ` | `A` | operand, send to output |
| `*` | `*` | `A` | push * |
| `B` | `*` | `AB` | operand, send to output |
| `-` | `-` | `AB*` | pop * (higher or equal precedence), push - |
| `(` | `-(` | `AB*` | push ( |
| `C` | `-(` | `AB*C` | operand, send to output |
| `*` | `-(*` | `AB*C` | push * |
| `D` | `-(*` | `AB*CD` | operand, send to output |
| `-` | `-(-` | `AB*CD*` | pop * (higher or equal precedence), push - |
| `(` | `-(-(` | `AB*CD*` | push ( |
| `E` | `-(-(` | `AB*CD*E` | operand, send to output |
| `/` | `-(-(/` | `AB*CD*E` | push / |
| `F` | `-(-(/` | `AB*CD*EF` | operand, send to output |
| `)` | `-(-` | `AB*CD*EF/` | pop to output until (: / |
| `$` | `-(-$` | `AB*CD*EF/` | push $ |
| `G` | `-(-$` | `AB*CD*EF/G` | operand, send to output |
| `*` | `-(-*` | `AB*CD*EF/G$` | pop $ (higher or equal precedence), push * |
| `H` | `-(-*` | `AB*CD*EF/G$H` | operand, send to output |
| `)` | `-` | `AB*CD*EF/G$H*-` | pop to output until (: * - |
| `-` | `-` | `AB*CD*EF/G$H*--` | pop - (higher or equal precedence), push - |
| `I` | `-` | `AB*CD*EF/G$H*--I` | operand, send to output |
| `end` | ` ` | `AB*CD*EF/G$H*--I-` | pop the remaining operators: - |

$$\boxed{\,\text{Postfix} = \mathtt{AB*CD*EF/G\$H*\text{-}\text{-}I\text{-}}\,}$$

(Check: `AB*CD*EF/G$H*--I-` was evaluated by computer for random values and always gives the same number as the infix expression.)

**Recursion tree for the 4th Fibonacci term.** With $F(0) = 0$, $F(1) = 1$ and $F(n) = F(n-1) + F(n-2)$:

```
FIB(n)
  if n <= 1: return n
  return FIB(n-1) + FIB(n-2)
```

```figure caption="Recursion tree for F(4) with F(0) = 0 and F(1) = 1 (blue boxes are the base cases, each box shows the returned value)."
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
T=('F(4)=3', 'call', [('F(3)=2', 'call', [('F(2)=1', 'call', [('F(1)=1', 'base', []), ('F(0)=0', 'base', [])]), ('F(1)=1', 'base', [])]), ('F(2)=1', 'call', [('F(1)=1', 'base', []), ('F(0)=0', 'base', [])])])
fig,ax=plt.subplots(figsize=(5.6,3.3)); ax.axis("off")
gtree(ax,T,dx=1.0,dy=1.1,w=0.95,fs=7)
```

The tree has 9 calls (4 internal calls and 5 base cases: $F(1)$ three times and $F(0)$ twice), and the answer is $F(4) = 3$ (the sequence 0, 1, 1, 2, 3, ...; the fourth term counted from $F(1)$ is $F(3) = 2$, which is the left subtree of the tree). $F(2)$ is computed twice and $F(1)$ three times: the number of calls grows like $\varphi^{n}$, so plain recursion is $O(2^{n})$, whereas memoisation or a loop gives $O(n)$.

@s 3
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

@s 4
**Why a linked list has no random access.** The nodes of a linked list lie anywhere in memory and the only way to find a node is to follow the `next` pointers from the head. There is no address formula like the array's $\text{address}(a[i]) = \text{base} + i \times \text{size}$.

Example: list `head -> 10 -> 20 -> 30 -> 40 -> 50 -> NULL`. To read the 4th item (40) we start at the head and move three times: head $\to$ 10 $\to$ 20 $\to$ 30 $\to$ 40, i.e. $k - 1 = 3$ pointer hops, while an array reads `a[3]` in one step. Reaching the $k$-th node costs $O(k)$, up to $O(n)$ for the last node (average $n/2$ hops), against $O(1)$ for an array; the same applies to binary search, which is therefore impractical on a linked list.

**Addition of polynomials using a linked list.**

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

@s 5
**(a) Linked list.** A linked list is a linear collection of nodes in which each node holds data and a pointer (link) to the next node; the first node is reached through `head`, the last node's pointer is NULL. Nodes are created at run time, so the list can grow and shrink freely.

**Dynamic stack with a singly linked list.** The `top` pointer points to the head of the list, so both push and pop work at the head in $O(1)$ time, and the stack is full only when memory is exhausted.

```
PUSH(x)                                  POP()
1. new = allocate a node                 1. if top == NULL: underflow, return
2. if new == NULL: overflow, return      2. t = top
3. new.data = x                          3. x = t.data
4. new.next = top                        4. top = top.next
5. top = new                             5. free(t);  return x
```

```figure caption="Dynamic stack as a singly linked list after push(40): top points to the newest node; pop removes the node at top."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
def cell(ax,x,y,w,h,t,fc="white",fs=8):
    ax.add_patch(mp.Rectangle((x,y-h/2),w,h,fc=fc,ec=INK,lw=1.2,zorder=3)); ax.text(x+w/2,y,t,ha="center",va="center",fontsize=fs,zorder=4)
fig,ax=plt.subplots(figsize=(6.0,1.5)); ax.axis("off"); ax.set_xlim(-0.3,11.6); ax.set_ylim(-1.1,1.1)
V=[40,30,20,10]
ax.text(0.1,0,"top",fontsize=8,va="center",color=ACCENT); arr(ax,(0.7,0),(1.2,0))
for i,v in enumerate(V):
    x=1.2+i*2.6
    cell(ax,x,0,1.0,0.7,str(v),fc="#fff4d6" if i==0 else "#eaf3ff"); cell(ax,x+1.0,0,0.6,0.7,"")
    ax.plot([x+1.3],[0],"o",color=ACCENT,ms=3.5,zorder=5)
    if i<3: arr(ax,(x+1.3,0),(x+2.6,0))
    else: ax.text(x+1.95,0,"NULL",fontsize=7.5,va="center")
```

```
#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int data; struct Node *next; } Node;
Node *top = NULL;                                  /* empty stack */

void push(int x) {
    Node *n = malloc(sizeof(Node));                /* 1. create a node */
    if (n == NULL) { printf("overflow: no memory\n"); return; }
    n->data = x;                                   /* 2. store the data */
    n->next = top;                                 /* 3. new node points to the old top */
    top = n;                                       /* 4. top moves to the new node */
}

int pop(void) {
    if (top == NULL) { printf("underflow: stack empty\n"); return -1; }
    Node *t = top;                                 /* 1. remember the top node */
    int x = t->data;                               /* 2. take its data */
    top = top->next;                               /* 3. move top down */
    free(t);                                       /* 4. release the node */
    return x;
}

int main(void) {
    push(10); push(20); push(30);
    printf("pop -> %d\n", pop());
    printf("pop -> %d\n", pop());
    push(40);
    printf("pop -> %d\n", pop());
    printf("pop -> %d\n", pop());
    pop();
    return 0;
}
```

Output of the program (compiled with gcc and run):

```
pop -> 30
pop -> 20
pop -> 40
pop -> 10
underflow: stack empty
```

**(b) Insertion at a given position in a doubly linked list.** Each node has `prev`, `data` and `next`. To insert at position $pos$ (1-based):

```
INSERT-AT(head, pos, x)
1. new = allocate a node;  new.data = x
2. if pos == 1:                               // insert at the beginning
       new.prev = NULL;  new.next = head
       if head != NULL: head.prev = new
       head = new;  return
3. t = head;  move t forward pos - 2 times (to node number pos - 1)
4. if t == NULL: position out of range, return
5. new.next = t.next                          // new points forward to the old successor
6. new.prev = t                               // new points back to t
7. if t.next != NULL: t.next.prev = new       // old successor points back to new
8. t.next = new                               // t points forward to new
```

```figure caption="Doubly linked list: inserting 25 at position 3 (between 20 and 30). The four pointer updates are listed in the algorithm."
import numpy as _np, matplotlib.patches as mp
def box(ax,x,y,w,h,t,fc="white",ec=INK,fs=8,lw=1.2,ls="-"):
    ax.add_patch(mp.FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",fc=fc,ec=ec,lw=lw,ls=ls,zorder=3))
    ax.text(x,y,t,ha="center",va="center",fontsize=fs,zorder=4)
def arr(ax,a,b,c=None,rad=0.0,lw=1.2,sa=0,sb=0,style="-|>"):
    ax.annotate("",xy=b,xytext=a,arrowprops=dict(arrowstyle=style,color=c or ACCENT,lw=lw,shrinkA=sa,shrinkB=sb,connectionstyle="arc3,rad=%s"%rad),zorder=2)
def cell(ax,x,y,w,h,t,fc="white",fs=8):
    ax.add_patch(mp.Rectangle((x,y-h/2),w,h,fc=fc,ec=INK,lw=1.2,zorder=3)); ax.text(x+w/2,y,t,ha="center",va="center",fontsize=fs,zorder=4)
fig,ax=plt.subplots(figsize=(6.8,2.6)); ax.axis("off"); ax.set_xlim(-0.2,13.6); ax.set_ylim(-2.3,2.2)
def dn(x,y,v,fc="#eaf3ff"):
    cell(ax,x,y,0.5,0.6,"",fc="white"); cell(ax,x+0.5,y,0.8,0.6,str(v),fc=fc); cell(ax,x+1.3,y,0.5,0.6,"",fc="white")
def row(vals,y,hi=None):
    xs=[]
    for i,v in enumerate(vals):
        x=0.3+i*2.6; xs.append(x); dn(x,y,v,fc="#fff4d6" if v==hi else "#eaf3ff")
    for i in range(len(vals)-1):
        arr(ax,(xs[i]+1.55,y+0.12),(xs[i+1]+0.02,y+0.12),sa=0,sb=0); arr(ax,(xs[i+1]+0.25,y-0.12),(xs[i]+1.78,y-0.12),sa=0,sb=0,c="#b00020")
row([10,20,30,40],1.2); ax.text(11.2,1.2,"before",fontsize=8,va="center")
row([10,20,25,30,40],-1.2,hi=25); ax.text(13.0,-1.2,"after",fontsize=7,va="center",ha="right")
```

```
#include <stdio.h>
#include <stdlib.h>

typedef struct Node { int data; struct Node *prev, *next; } Node;

Node *insert_at(Node *head, int pos, int x) {      /* pos is 1-based */
    Node *n = malloc(sizeof(Node));
    n->data = x; n->prev = n->next = NULL;
    if (pos == 1) {                                /* insertion at the beginning */
        n->next = head;
        if (head != NULL) head->prev = n;
        return n;
    }
    Node *t = head;
    for (int i = 1; i < pos - 1 && t != NULL; i++) t = t->next;   /* stop at node pos-1 */
    if (t == NULL) { printf("position out of range\n"); free(n); return head; }
    n->next = t->next;                             /* new -> next = node after t */
    n->prev = t;                                   /* new -> prev = t */
    if (t->next != NULL) t->next->prev = n;        /* old next points back to new */
    t->next = n;                                   /* t points forward to new */
    return head;
}

void show(Node *h) {
    Node *last = NULL;
    printf("forward : ");
    for (; h != NULL; last = h, h = h->next) printf("%d ", h->data);
    printf("\nbackward: ");
    for (; last != NULL; last = last->prev) printf("%d ", last->data);
    printf("\n");
}

int main(void) {
    Node *head = NULL;
    head = insert_at(head, 1, 10); head = insert_at(head, 2, 20);
    head = insert_at(head, 3, 30); head = insert_at(head, 4, 40);
    show(head);
    head = insert_at(head, 3, 25);                 /* insert 25 at position 3 */
    show(head);
    head = insert_at(head, 1, 5);                  /* insert at the front */
    head = insert_at(head, 7, 50);                 /* insert at the end */
    show(head);
    return 0;
}
```

Output of the program (compiled with gcc and run):

```
forward : 10 20 30 40 
backward: 40 30 20 10 
forward : 10 20 25 30 40 
backward: 40 30 25 20 10 
forward : 5 10 20 25 30 40 50 
backward: 50 40 30 25 20 10 5
```

**Polynomial as a linked list.** One node per non-zero term with fields `coef`, `exp`, `next`, the terms ordered by decreasing exponent. For example $3x^{4} + 2x^{2} + 5x + 1$ is the list $(3,4) \to (2,2) \to (5,1) \to (1,0) \to \text{NULL}$, shown below (the missing $x^{3}$ term needs no node, so a sparse polynomial uses little memory).

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

@s 6
**Minimum spanning tree.** For a connected, weighted, undirected graph with $V$ vertices, a spanning tree is a subgraph that is a tree containing all $V$ vertices (exactly $V - 1$ edges, no cycle). A **minimum spanning tree (MST)** is the spanning tree whose total edge weight is the smallest.

**Kruskal's algorithm** (greedy, edges globally sorted):

```
KRUSKAL(G)
  1. T = empty set
  2. for each vertex v: MAKE-SET(v)                  // every vertex is its own component
  3. sort the edges in non-decreasing order of weight
  4. for each edge (u, v) in that order
         if FIND-SET(u) != FIND-SET(v):              // the edge joins two components (no cycle)
             add (u, v) to T;  UNION(u, v)
         if |T| == V - 1: stop
  5. return T                                         // time O(E log E)
```

For the given graph (vertices A to F; edges AB 4, AC 5, BD 9, BC 11, BE 7, CE 3, DE 13, DF 2, EF 6) the algorithm gives:

| # | Edge | Weight | Decision |
|---|---|---|---|
| 1 | DF | 2 | accept |
| 2 | CE | 3 | accept |
| 3 | AB | 4 | accept |
| 4 | AC | 5 | accept |
| 5 | EF | 6 | accept |
| 6 | BE | 7 | reject (cycle) |
| 7 | BD | 9 | reject (cycle) |
| 8 | BC | 11 | reject (cycle) |
| 9 | DE | 13 | reject (cycle) |

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

MST edges: DF (2), CE (3), AB (4), AC (5), EF (6), total weight $2 + 3 + 4 + 5 + 6 = 20$.

**Dijkstra's algorithm from A to F.** Set $d(A) = 0$ and all other labels $\infty$. Repeatedly make permanent the vertex with the smallest tentative distance and relax its edges, $d(v) = \min(d(v), d(u) + w(u,v))$.

| Step | Vertex made permanent | Tentative distances of the others |
|---|---|---|
| 1 | A (d = ) | B = 4, C = 5, D = ∞, E = ∞, F = ∞ |
| 2 | B (d = ) | C = 5, D = 13, E = 11, F = ∞ |
| 3 | C (d = ) | D = 13, E = 8, F = ∞ |
| 4 | E (d = ) | D = 13, F = 14 |
| 5 | D (d = ) | F = 14 |
| 6 | F (d = ) |  |

| Vertex | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| Shortest distance from A | 0 | 4 | 5 | 13 | 8 | 14 |

Tracing the predecessors back from F: $F \leftarrow E \leftarrow C \leftarrow A$.

```figure caption="Shortest-path tree from A (thick): the route to F is A-C-E-F with length 14."
E=[('A', 'B', 4), ('A', 'C', 5), ('B', 'D', 9), ('B', 'C', 11), ('B', 'E', 7), ('D', 'E', 13), ('D', 'F', 2), ('C', 'E', 3), ('E', 'F', 6)]
M=[('B', 'A'), ('C', 'A'), ('D', 'B'), ('E', 'C'), ('F', 'E')]
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

$$\boxed{\,\text{Shortest path A} \to \text{F} = A - C - E - F \text{ with length } 5 + 3 + 6 = 14\,}$$

(The other routes are longer: A-B-D-F = 4 + 9 + 2 = 15, A-B-E-F = 4 + 7 + 6 = 17, A-C-B-D-F = 27.)

@s 7
**In-place and not-in-place sorting.**

- An **in-place** sorting algorithm rearranges the elements inside the given array using only a constant (or very small, e.g. $O(\log n)$) amount of extra memory. Examples: bubble, selection, insertion, heap sort and quick sort (extra memory only for the recursion stack).
- A **not-in-place** (out-of-place) algorithm needs additional memory that grows with the input, typically a second array of size $n$. Examples: merge sort ($O(n)$ auxiliary array), counting sort, radix and bucket sort.

In-place algorithms save memory; not-in-place ones (merge sort) can offer stability and guaranteed $O(n \log n)$ time.

**Quick sort** is a divide-and-conquer algorithm: choose a pivot (here the first element), partition so that the smaller-or-equal keys lie to its left and the larger keys to its right (the pivot is then in its final place), and sort the two parts recursively.

```
QUICKSORT(A, lo, hi)
  if lo < hi
      p = A[lo];  i = lo + 1;  j = hi
      repeat
          while i <= hi and A[i] <= p: i = i + 1        // find an element larger than the pivot
          while A[j] > p:               j = j - 1        // find an element not larger than the pivot
          if i < j: swap A[i], A[j]
      until i >= j
      swap A[lo], A[j]                                    // pivot into its final position j
      QUICKSORT(A, lo, j - 1);  QUICKSORT(A, j + 1, hi)
```

Data: 20, 50, 40, 30, 10, 90, 80, 35.

| Sub-list (positions) | Pivot | Pivot final position | Array after the partition |
|---|---|---|---|
| 1 to 8 | 20 | 2 | 10, 20, 40, 30, 50, 90, 80, 35 |
| 3 to 8 | 40 | 5 | 10, 20, 35, 30, 40, 90, 80, 50 |
| 3 to 4 | 35 | 4 | 10, 20, 30, 35, 40, 90, 80, 50 |
| 6 to 8 | 90 | 8 | 10, 20, 30, 35, 40, 50, 80, 90 |
| 6 to 7 | 50 | 6 | 10, 20, 30, 35, 40, 50, 80, 90 |

Detail of the first partition (pivot 20): $i$ stops at 50, $j$ stops at 10; they are swapped giving 20, 10, 40, 30, 50, 90, 80, 35; then $i$ stops at 40 and $j$ moves left to the 10 at position 2, so $j < i$ and the pivot 20 is swapped with A[j] = 10, which gives 10, 20, 40, 30, 50, 90, 80, 35. Sorting continues on the part to the right of 20 (positions 3 to 8) with pivot 40, and so on.

$$\boxed{\,\text{Sorted: } 10,\ 20,\ 30,\ 35,\ 40,\ 50,\ 80,\ 90\,}$$

Average time $O(n \log n)$, worst case $O(n^{2})$ (already sorted input with the first element as pivot).

@s 8
**Hashing** is a technique that stores each record in a table at an address computed from its key by a **hash function** $h(k)$, so that insertion and search take $O(1)$ time on average without comparing keys one by one. Two keys with the same hash value collide; a collision is resolved by open addressing (linear or quadratic probing, double hashing) or by chaining.

**Binary search algorithm** (sorted array): compare the key with the middle element and continue in the left or the right half.

```
BINARY-SEARCH(A, n, key)
  low = 0;  high = n - 1
  while low <= high
      mid = (low + high) / 2
      if A[mid] == key:  return mid
      else if key < A[mid]:  high = mid - 1
      else:                  low = mid + 1
  return -1
```

Time $O(\log n)$ (about $\log_2 n + 1$ comparisons in the worst case), space $O(1)$. A C program with a trace:

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

**Linear probing.** $h(k) = k \bmod 10$; if cell $h(k)$ is occupied, try $(h(k) + i) \bmod 10$ for $i = 1, 2, 3, \dots$ (the next cell).

| Key | h(k) = k mod 10 | Probe positions tried ((h + i) mod 10) | Stored at |
|---|---|---|---|
| 12 | 2 | 2 | **2** |
| 22 | 2 | 2, 3 | **3** |
| 34 | 4 | 4 | **4** |
| 41 | 1 | 1 | **1** |
| 53 | 3 | 3, 4, 5 | **5** |
| 64 | 4 | 4, 5, 6 | **6** |
| 79 | 9 | 9 | **9** |

Table after each insertion (state at the end):

| Index | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| Key | - | 41 | 12 | 22 | 34 | 53 | 64 | - | - | 79 |

$$\boxed{\,\text{Table: } 1 \to 41,\ 2 \to 12,\ 3 \to 22,\ 4 \to 34,\ 5 \to 53,\ 6 \to 64,\ 9 \to 79\,}$$

Keys 22 (collision with 12), 53 (collides with 22 and 34) and 64 (collides with 34 and 53) were moved to the next free cell. Note the primary clustering in cells 2 to 6; the average search cost grows as the cluster grows.
