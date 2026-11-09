"""Second paper (2082 Bhadra) + writes both md files.  python3 gen_dsa2.py <outdir>"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_dsa import *

PF2, PFR2 = to_postfix("A*B-(C*D-(E/F)$G*H)-I"); eval_check("A*B-(C*D-(E/F)$G*H)-I", PF2)
assert PF2 == "AB*CD*EF/G$H*--I-"
qs_sorted, qs_log = quicksort([20, 50, 40, 30, 10, 90, 80, 35])
lp_t, lp_rows = hash_insert([12, 22, 34, 41, 53, 64, 79], 10, lambda i: i)
dj_md = dijk_md(rows_g, None)
kr_md = "| # | Edge | Weight | Decision |\n|---|---|---|---|\n" + "".join("| %d | %s%s | %d | %s |\n" % (i, u, v, w, d) for i, (u, v, w, d) in enumerate(krows, 1))
sp = []
x = "F"
while x in prev_g: sp.append(x); x = prev_g[x]
sp.append(x); sp.reverse()
assert sp == ["A", "C", "E", "F"]
res_tbl = "| Vertex | A | B | C | D | E | F |\n|---|---|---|---|---|---|---|\n| Shortest distance from A | " + " | ".join(str(dist_g[v]) for v in "ABCDEF") + " |\n"

D2 = r'''---
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

''' + FIG_GQ + r'''
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

''' + growth_md() + r'''
(Values are the number of basic steps; $2^{n}$ for $n = 100$ and $n = 1000$ is astronomically large, which is why exponential algorithms are impractical.) The usual order is $1 < \log n < n < n \log n < n^{2} < n^{3} < 2^{n} < n!$.

@s 2
**Reading the expression.** The operator `$` means exponentiation (highest precedence, right associative, written `^` in other papers), then come `*` and `/`, then `+` and `-`. So `$` binds tighter than `*`: the expression is `A*B - (C*D - ((E/F) $ G) * H) - I`. Rules: operands go straight to the output; `(` is pushed; `)` pops to the output until `(`; an operator pops every operator of higher or equal precedence (for `$`, only strictly higher) and is pushed; at the end everything left is popped.

''' + postfix_md(PFR2) + r'''
$$\boxed{\,\text{Postfix} = \mathtt{AB*CD*EF/G\$H*\text{-}\text{-}I\text{-}}\,}$$

(Check: `AB*CD*EF/G$H*--I-` was evaluated by computer for random values and always gives the same number as the infix expression.)

**Recursion tree for the 4th Fibonacci term.** With $F(0) = 0$, $F(1) = 1$ and $F(n) = F(n-1) + F(n-2)$:

```
FIB(n)
  if n <= 1: return n
  return FIB(n-1) + FIB(n-2)
```

''' + fib_fig(4) + r'''
The tree has 9 calls (4 internal calls and 5 base cases: $F(1)$ three times and $F(0)$ twice), and the answer is $F(4) = 3$ (the sequence 0, 1, 1, 2, 3, ...; the fourth term counted from $F(1)$ is $F(3) = 2$, which is the left subtree of the tree). $F(2)$ is computed twice and $F(1)$ three times: the number of calls grows like $\varphi^{n}$, so plain recursion is $O(2^{n})$, whereas memoisation or a loop gives $O(n)$.

@s 3
''' + CQ_TEXT + r'''
@s 4
**Why a linked list has no random access.** The nodes of a linked list lie anywhere in memory and the only way to find a node is to follow the `next` pointers from the head. There is no address formula like the array's $\text{address}(a[i]) = \text{base} + i \times \text{size}$.

Example: list `head -> 10 -> 20 -> 30 -> 40 -> 50 -> NULL`. To read the 4th item (40) we start at the head and move three times: head $\to$ 10 $\to$ 20 $\to$ 30 $\to$ 40, i.e. $k - 1 = 3$ pointer hops, while an array reads `a[3]` in one step. Reaching the $k$-th node costs $O(k)$, up to $O(n)$ for the last node (average $n/2$ hops), against $O(1)$ for an array; the same applies to binary search, which is therefore impractical on a linked list.

**Addition of polynomials using a linked list.**

''' + POLY_TEXT + r'''
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

''' + FIG_STACK + r'''
''' + code(STACK_C, OUT_STACK) + r'''
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

''' + FIG_DLL + r'''
''' + code(DLL_C, OUT_DLL) + r'''
**Polynomial as a linked list.** One node per non-zero term with fields `coef`, `exp`, `next`, the terms ordered by decreasing exponent. For example $3x^{4} + 2x^{2} + 5x + 1$ is the list $(3,4) \to (2,2) \to (5,1) \to (1,0) \to \text{NULL}$, shown below (the missing $x^{3}$ term needs no node, so a sparse polynomial uses little memory).

''' + FIG_POLY + r'''
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

''' + kr_md + r'''
''' + FIG_MST + r'''
MST edges: DF (2), CE (3), AB (4), AC (5), EF (6), total weight $2 + 3 + 4 + 5 + 6 = 20$.

**Dijkstra's algorithm from A to F.** Set $d(A) = 0$ and all other labels $\infty$. Repeatedly make permanent the vertex with the smallest tentative distance and relax its edges, $d(v) = \min(d(v), d(u) + w(u,v))$.

''' + dj_md + r'''
''' + res_tbl + r'''
Tracing the predecessors back from F: $F \leftarrow E \leftarrow C \leftarrow A$.

''' + FIG_SPT + r'''
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

''' + qs_md(qs_log) + r'''
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

''' + code(BS_C, OUT_BS) + r'''
**Linear probing.** $h(k) = k \bmod 10$; if cell $h(k)$ is occupied, try $(h(k) + i) \bmod 10$ for $i = 1, 2, 3, \dots$ (the next cell).

''' + hash_md(lp_rows, "(h + i) mod 10") + r'''
Table after each insertion (state at the end):

''' + table_md(lp_t) + r'''
$$\boxed{\,\text{Table: } 1 \to 41,\ 2 \to 12,\ 3 \to 22,\ 4 \to 34,\ 5 \to 53,\ 6 \to 64,\ 9 \to 79\,}$$

Keys 22 (collision with 12), 53 (collides with 22 and 34) and 64 (collides with 34 and 53) were moved to the next free cell. Note the primary clustering in cells 2 to 6; the average search cost grows as the cluster grows.
'''
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, "ioe-enct252-2083-baishakh.md"), "w").write(D1)
open(os.path.join(OUT, "ioe-enct252-2082-bhadra.md"), "w").write(D2)
print("written", len(D1), len(D2))
