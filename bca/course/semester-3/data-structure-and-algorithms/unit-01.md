---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 1
title: Introduction to Data Structure
hours: 2
area: BCA 201 · Data Structure and Algorithms · Unit 1
---

Every program stores data and does something with it. A **data structure** is a disciplined way of organising data so that the operations you need are fast and simple; an **algorithm** is the step-by-step procedure that uses it. Choosing the right structure is usually the difference between a program that answers instantly and one that never finishes.

::: key What this unit gives you
- A precise definition of data structure and the standard classification.
- The idea of an Abstract Data Type (ADT): *what* a structure does, separated from *how*.
- A first look at measuring cost, which Unit 8 develops fully.
- A guide for choosing a structure, and the C conventions used in the rest of the book.
:::

## 1.1 Data, data structure and algorithm

**Data** are raw values (a roll number, a name, a mark). A **data structure** is a collection of data values, the relationships among them, and the operations that can be applied to them. An array of marks, a list of students and a tree of folders are data structures. An **algorithm** is a finite sequence of unambiguous steps that takes input and produces output, and always stops. Niklaus Wirth's slogan sums up the subject: **Algorithms + Data Structures = Programs**.

### Classification

| Basis | Classes | Examples |
|---|---|---|
| Primitive or not | **Primitive** (built into the language) · **Non-primitive** (built from primitives) | `int`, `char`, `float` · array, struct, list, tree |
| Shape | **Linear** (elements in a sequence, one predecessor and one successor) · **Non-linear** (one element may link to many) | array, stack, queue, linked list · tree, graph |
| Size | **Static** (fixed size at compile time) · **Dynamic** (grows and shrinks at run time) | array · linked list |
| Order of access | **Sequential** · **Random** | tape, linked list · array |

Non-primitive linear structures covered in this book: arrays, stack, queue, list and linked list (Units 2–5). Non-linear: trees and graphs (Units 7 and 10).

## 1.2 Abstract Data Type

An **Abstract Data Type (ADT)** is a mathematical model of a data structure defined by *what it stores* and *what operations it supports*, with no mention of how it is coded. The user sees only the interface; the implementer is free to change the inside.

::: example Worked example: the Stack ADT
**Data:** a collection of items in which only the most recently added one is accessible.
**Operations:** `push(x)` add item · `pop()` remove and return the top · `peek()` read the top · `isEmpty()` · `isFull()`.
**Rules:** `pop` on an empty stack is an *underflow* error; `push` on a full one is an *overflow*.
The same ADT can be implemented with an array (Unit 2) or a linked list (Unit 5). A program that only calls `push` and `pop` does not change when the implementation does. That independence is the whole point of an ADT.
:::

In C an ADT becomes a `struct` plus a set of functions that take a pointer to it:

```c
typedef struct { int items[100]; int top; } Stack;   /* the representation */
void stack_init(Stack *s);                           /* the interface      */
void push(Stack *s, int x);
int  pop(Stack *s);
```

**Three levels of thought:** the *logical* level (the ADT), the *implementation* level (array or pointers), and the *application* level (the program that uses it).

## 1.3 Why data structures matter

Searching for a name among 1,000,000 records takes up to 1,000,000 comparisons in an unsorted array, about 20 in a sorted array using binary search, and about 1 in a good hash table. Same data, same question; the structure decides the cost.

| Need | Good structure | Why |
|---|---|---|
| Undo, bracket matching, expression evaluation | Stack | last in, first out |
| Print queue, CPU scheduling, BFS | Queue | first in, first out |
| Frequent insertion and deletion in the middle | Linked list | no shifting |
| Fast lookup by position | Array | O(1) indexing |
| Hierarchies (folders, HTML DOM), fast ordered search | Tree | O(log n) when balanced |
| Fast lookup by key | Hash table | O(1) on average |
| Networks, maps, dependencies | Graph | arbitrary relationships |

## 1.4 Measuring cost in one page

Two resources matter: **time** (how many basic steps) and **space** (how much memory). We count steps as a function of input size *n* and keep only the dominant term; this is **Big-O notation** (full treatment in Unit 8).

| Notation | Name | n = 1000 → steps (approx.) | Typical example |
|---|---|---|---|
| O(1) | constant | 1 | array index, stack push |
| O(log n) | logarithmic | 10 | binary search |
| O(n) | linear | 1,000 | linear search, list traversal |
| O(n log n) | linearithmic | 10,000 | merge sort |
| O(n²) | quadratic | 1,000,000 | bubble sort |
| O(2ⁿ) | exponential | astronomically large | brute-force subsets |

A **good algorithm** is *correct*, *finite*, *efficient* and *clear*. Compare two ways to sum 1 + 2 + … + n: a loop does n additions, O(n); the formula n(n+1)/2 does a constant number, O(1). Both are correct; one scales.

## 1.5 Conventions in this book

- All programs are in C (C11) and were compiled and run; the output shown is the real output.
- Arrays are indexed from 0. A stack's `top` is −1 when empty.
- Tree height counts **edges** on the longest root-to-leaf path: a single node has height 0, the empty tree −1.
- "Efficiency" means worst case unless the text says average.

## 1.6 Seeing the ideas: algorithms, structures and cost

Algorithms are older than computers. Around 300 BC the Greek mathematician Euclid wrote down, in his *Elements*, a procedure for finding the greatest common divisor of two numbers; it is still used, unchanged, inside every modern computer. The word *algorithm* itself comes from the name of the ninth-century scholar al-Khwarizmi. In the twentieth century Donald Knuth gathered the whole subject into the many volumes of *The Art of Computer Programming*, and the phrase "analysis of algorithms" is his. The photographs below connect the ideas of this unit to the people who shaped them.

```photogrid label="1.1" cols="2" ratio="1.25" caption="Two ends of the history of algorithms. (a) A fragment of Euclid's Elements on papyrus from Oxyrhynchus in Egypt (about 100 AD); the small diagram at the right is a geometric figure belonging to a proof. Euclid's method for the greatest common divisor is the oldest non-trivial algorithm still in everyday use. (b) Donald Knuth, who named and organised the analysis of algorithms and whose books taught several generations of programmers to count the cost of a program."
@ photo id="bca201/euclid" cap="Euclid's Elements, papyrus fragment"
fit 1.25
focus 0.5 0.5
call 0.72 0.45 0.04 0.9 "proof diagram"
@ photo id="bca201/knuth" cap="Donald E. Knuth"
fit 1.25
focus 0.5 0.4
```

```svgfig label="1.1" caption="Classification of data structures. Primitive types (int, char, float) are built into the language. Non-primitive structures are built from them. A linear structure keeps its items in a single sequence, so each item (except the first and last) has one predecessor and one successor; a non-linear structure branches. A static structure has a size fixed before the program runs (an array); a dynamic structure grows and shrinks at run time (a linked list). Every box here is studied in a later unit of this book."
f = Fig(580, 250)
f.box(215, 8, 150, 30, "Data structures", fill=NAVY, stroke=NAVY, color="#ffffff", size=11.5, bold=True)
f.box(70, 62, 150, 30, "Primitive", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.box(360, 62, 170, 30, "Non-primitive", fill=BLUE, stroke=NAVY, size=11, bold=True)
f.line(290, 38, 145, 62, color=SLATE); f.line(290, 38, 445, 62, color=SLATE)
f.text(145, 108, "int, char, float,\ndouble, pointer", size=9.5, color=SLATE)
f.box(300, 120, 130, 30, "Linear", fill=MINT, stroke=TEAL, size=11, bold=True)
f.box(450, 120, 120, 30, "Non-linear", fill=SAND, stroke=AMBER, size=11, bold=True)
f.line(445, 92, 365, 120, color=SLATE); f.line(445, 92, 510, 120, color=SLATE)
f.text(365, 172, "array, stack, queue,\nlinked list", size=9.5, color=TEAL, bold=True)
f.text(510, 172, "tree, graph", size=9.5, color=AMBER, bold=True)
f.box(300, 205, 130, 30, "Static: array", fill=SOFT, stroke=SLATE, size=10, bold=True)
f.box(440, 205, 130, 30, "Dynamic: linked list", fill=SOFT, stroke=SLATE, size=10, bold=True)
```

```svgfig label="1.2" caption="An Abstract Data Type separates the interface from the implementation. The Queue ADT promises four operations and one rule (first in, first out). The user's program, on the left, calls only those operations. Behind the wall the same ADT can be implemented with a circular array (Unit 3) or with a linked list (Unit 5); the program does not change when the implementation is swapped. This is why the ADT is described as what a structure does, never how."
f = Fig(580, 220)
f.box(10, 40, 150, 120, "User program\n\nenqueue(x)\ndequeue()\nisEmpty()", fill=BLUE, stroke=NAVY, size=10.5, bold=True)
f.box(215, 25, 150, 150, "", fill=SAND, stroke=AMBER, sw=1.8, dash=True)
f.text(290, 42, "Queue ADT (interface)", size=10.5, color=AMBER, bold=True)
f.text(290, 100, "enqueue, dequeue,\npeek, isEmpty\nrule: first in, first out", size=10, color=SLATE, bold=True)
f.box(420, 25, 150, 60, "Circular array\nfront, rear, size", fill=MINT, stroke=TEAL, size=10, bold=True)
f.box(420, 115, 150, 60, "Linked list\nhead and tail nodes", fill=MINT, stroke=TEAL, size=10, bold=True)
f.arrow([(160, 100), (215, 100)], color=NAVY, sw=1.6)
f.arrow([(365, 70), (420, 55)], color=TEAL, sw=1.6)
f.arrow([(365, 130), (420, 145)], color=TEAL, sw=1.6)
f.text(290, 200, "swap the box on the right without touching the box on the left", size=10, color=RED, bold=True)
```

```svgfig label="1.3" caption="How fast the cost of an algorithm grows with the input size n (bars drawn on a logarithmic scale; each step to the right is ten times more steps). For n = 1,000,000 an algorithm of cost log2 n needs about 20 steps, one of cost n needs 1,000,000, one of cost n log2 n needs about 19,931,569, and one of cost n squared needs 1,000,000,000,000. At one microsecond per step the last one takes 11.6 days while the first one takes 20 microseconds. This is why Big-O is the first question to ask about any algorithm."
import math
f = Fig(580, 240)
n = 1000000
rows = [("log2 n", math.log2(n), TEAL, MINT), ("n", n, NAVY, BLUE), ("n log2 n", n * math.log2(n), AMBER, SAND), ("n squared", n * n, RED, ROSE)]
f.text(290, 14, "steps for n = 1,000,000 (log scale, 1 step = shortest bar)", size=10.5, color=SLATE, bold=True)
for i, (nm, v, st, fl) in enumerate(rows):
    y = 34 + i * 48
    w = 40 + 60 * math.log10(v)
    f.text(8, y + 15, nm, size=10.5, color=st, bold=True, anchor="start")
    f.box(100, y, w, 30, "{:,.0f}".format(v), fill=fl, stroke=st, size=10.5, bold=True)
f.text(290, 228, "log2 n = 19.93, n log2 n = 19,931,569 (rounded to whole steps)", size=9.5, color=SLATE)
```

### 1.6.1 Eight applications of data structures in everyday Nepali systems

1. **Arrays store tabular records.** The marks sheet of a TU examination, a list of ward numbers or the days of a Bikram Sambat month are all arrays. An array gives instant access to the i-th element by its index. Because the size is fixed, it suits data whose length is known in advance.
2. **Stacks undo and go back.** When you press the back button in a browser or on the Nagarik App, the last screen you visited is the first one you return to. The same last-in, first-out rule powers the undo command in a word processor. The function call stack of every C program is also a stack.
3. **Queues keep things fair.** A bank token system, a ticket line at a railway counter and the print queue of a college computer lab all serve the oldest request first. Fonepay and ConnectIPS servers also queue payment requests so that none is lost during a busy festival evening. A queue guarantees first come, first served.
4. **Linked lists grow without waste.** A music playlist or the list of open windows can grow and shrink while the program runs. Inserting a node needs only a few pointer changes and no shifting of other items. This makes linked lists suitable when the number of items is not known beforehand.
5. **Trees show hierarchy.** The folders of a computer, the organisation chart of Tribhuvan University (the university, faculties, campuses, departments) and the HTML of a web page are trees. A binary search tree also finds a name among thousands in about a dozen comparisons. Trees combine hierarchy with fast searching.
6. **Graphs model connections.** A road map of the Kathmandu valley, the network of Nepal Telecom towers and the friends of a social-media user are graphs. Route finders such as the one used by ride-hailing apps run shortest-path algorithms on a graph. Whenever the question is "how are these things connected", a graph is the answer.
7. **Hash tables give instant lookup.** A login system finds your account from your username, and a government portal finds a record from a citizenship number, without scanning every record. A hash function converts the key into a table position in one step. Average lookup time is therefore almost constant.
8. **Priority queues serve the most urgent first.** An emergency ward triages patients by severity, not by arrival time, and an operating system runs the highest-priority process first. A heap implements this efficiently, so the most urgent item can be removed in logarithmic time. This is the structure behind scheduling and event simulation.

## Formula and fact sheet

- Data structure = data + relationships + operations. ADT = operations without implementation.
- Linear: array, list, stack, queue. Non-linear: tree, graph.
- Growth order: 1 ≪ log n ≪ n ≪ n log n ≪ n² ≪ 2ⁿ ≪ n!.
- Σ 1..n = n(n+1)/2.

## Chapter summary

- A data structure organises data for efficient operations; an algorithm is a finite, unambiguous procedure.
- Structures are classified as primitive/non-primitive, linear/non-linear, static/dynamic.
- An ADT specifies behaviour only, so implementations can be swapped.
- The right structure changes cost from linear to logarithmic or constant; Big-O is the common yardstick.

## Practice

1. Define data structure and algorithm. State two differences.
2. Classify: array, stack, tree, graph, `int`, linked list.
3. What is an ADT? Give the ADT of a queue (data, operations, rules).
4. Why is a linked list called dynamic while an array is static?
5. Which structure would you choose for (a) browser back button, (b) a printer spooler, (c) a family tree, (d) phone book lookup by name? Justify.
6. Count the steps of summing 1..n by a loop versus by formula, and give the Big-O of each.
7. If an algorithm takes 3n² + 5n + 7 steps, what is its Big-O?
8. How many comparisons does binary search need, at most, to search 1,000,000 sorted items?

::: note Answers and worked solutions
**1.** A data structure is a way of organising data with its operations; an algorithm is a finite sequence of steps to solve a problem. The structure holds data; the algorithm acts on it.
**2.** Array: non-primitive, linear, static. Stack: non-primitive, linear, dynamic or static by implementation. Tree and graph: non-primitive, non-linear. `int`: primitive. Linked list: non-primitive, linear, dynamic.
**3.** Queue ADT: data = items in arrival order; operations = enqueue (add at rear), dequeue (remove from front), front, isEmpty, isFull; rule = first in, first out; dequeue on empty is underflow.
**4.** A linked list allocates each node when needed (`malloc`) and frees it when done, so its size follows the data. An array size is fixed at declaration.
**5.** (a) Stack, last page visited is first to return. (b) Queue, first job submitted prints first. (c) Tree, one parent to many children. (d) Hash table or sorted array with binary search, fast key lookup.
**6.** Loop: n additions → O(n). Formula: one multiplication, one addition, one division → O(1).
**7.** Drop the constants and lower terms: **O(n²)**.
**8.** ⌈log₂ 1,000,000⌉ ≈ **20** comparisons (2²⁰ = 1,048,576).
:::

## Model answers (5 and 10 marks)

**Q1. Define data structure and explain its classification. (5 marks)**

A **data structure** is a systematic way of organising and storing data in memory so that the operations a program needs, such as insertion, deletion, searching and traversal, can be done efficiently. An **algorithm** is the finite sequence of steps that works on that data. The two always go together: a good algorithm on a poor structure is still slow.

Data structures are classified in the following way (Figure 1.1).
- **Primitive structures** are built into the language: `int`, `char`, `float`, `double` and pointers. The machine understands them directly.
- **Non-primitive structures** are built from primitive ones. They are divided into **linear** structures (array, stack, queue, linked list), in which items form one sequence, and **non-linear** structures (tree, graph), in which one item may be connected to many.
- By memory use they are also **static** (size fixed at compile time, such as an array) or **dynamic** (size changes at run time, such as a linked list).

For example, a marks sheet of 40 students is naturally an array, while the folders of a college file server form a tree. Choosing the right structure is the first design decision of any program.

**Q2. What is an Abstract Data Type? Explain with the example of a stack. (5 marks)**

An **Abstract Data Type (ADT)** is a mathematical description of a data structure in terms of its data, its operations and the rules those operations obey, without saying how it is implemented in memory. It tells the user *what* the structure does and hides *how* it does it. This hiding is called **abstraction** and it gives two benefits: the user cannot damage the internals, and the implementation can be changed without changing the programs that use it (Figure 1.2).

The **Stack ADT** has the following definition.
- **Data:** an ordered collection of items with one end called the top.
- **Operations:** `push(x)` adds x at the top, `pop()` removes and returns the top item, `peek()` reads the top without removing it, `isEmpty()` and `isFull()` test the state.
- **Rule:** last in, first out (LIFO). Popping an empty stack is an *underflow*; pushing onto a full stack is an *overflow*.

The same ADT can be implemented with an array and an integer `top` (Unit 2) or with a linked list whose head is the top (Unit 5). A program that only calls `push` and `pop` works with both. In C the usual way to build an ADT is a `struct` plus a set of functions that receive a pointer to it.

**Q3. Explain data structure, its types and importance, and describe how the efficiency of an algorithm is judged. (10 marks)**

**Introduction.** Programs store data and process it. A data structure organises the data so that processing is fast and simple; an algorithm is the procedure that does the processing. Together, in the words of Niklaus Wirth, algorithms plus data structures make programs.

**Classification.** Figure 1.1 shows that data structures are primitive or non-primitive, the latter being linear (array, stack, queue, linked list) or non-linear (tree, graph), and static or dynamic according to when their size is fixed.

**Abstract Data Type.** Each structure is specified as an ADT, meaning data, operations and rules without implementation detail, so that the interface stays stable while the implementation may change (Figure 1.2).

**Why the choice matters.** To find one roll number among 1,000,000 sorted records, linear search needs up to 1,000,000 comparisons, while binary search needs at most 20. The same data held in an unsorted linked list cannot be searched by halving at all. The structure therefore decides which algorithms are possible.

**Judging efficiency.** An algorithm is judged by its **time complexity** (how many basic steps it takes as the input size n grows) and its **space complexity** (how much extra memory it uses). We count steps instead of seconds because seconds depend on the machine. We keep only the dominant term, so 3n squared plus 5n plus 7 is written O(n squared). Figure 1.3 shows the effect: for n = 1,000,000 an O(log n) method needs about 20 steps but an O(n squared) method needs 10 to the power 12, which is about 11.6 days at one microsecond per step.

| Structure | Access by position | Search | Insert at end | Best use |
|---|---|---|---|---|
| Array | O(1) | O(n); O(log n) if sorted | O(1) if space | Fixed tables |
| Linked list | O(n) | O(n) | O(1) with tail pointer | Growing lists |
| Stack / queue | top or ends only | O(n) | O(1) | Undo, scheduling |
| Binary search tree | O(log n) on average | O(log n) on average | O(log n) on average | Ordered data |
| Hash table | by key | O(1) on average | O(1) on average | Fast lookup |

**Conclusion.** A data structure is chosen by asking which operations are most frequent and what cost is acceptable. Understanding structures, ADTs and Big-O together lets a programmer write software that stays fast as data grows, such as a results system that must serve every TU student at once.
