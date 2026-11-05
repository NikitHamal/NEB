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
