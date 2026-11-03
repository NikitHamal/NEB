---
subject: Data Structure and Algorithms
grade: BCA Semester 3
unit: 6
title: Recursion
hours: 4
area: BCA 201 · Data Structure and Algorithms · Unit 6
---

**Recursion** is a technique in which a function solves a problem by calling itself on a smaller instance of the same problem. It is the natural way to write algorithms on trees, graphs and divide-and-conquer methods, and understanding it is essential for Units 7 to 11.

::: key What this unit gives you
- The two parts of every recursive definition and how the call stack executes it.
- Classic examples with tested code: factorial, Fibonacci, GCD, power, binary search, Towers of Hanoi.
- Recursion versus iteration, with costs.
- Backtracking and search trees, using the N-queens problem.
:::

## 6.1 Principle of recursion

A correct recursive function has:

1. **Base case(s):** inputs solved directly, without a further call. Without one the recursion never stops.
2. **Recursive case:** reduces the problem toward a base case and combines the results.

**Factorial:** 0! = 1 (base); n! = n × (n − 1)! (recursive). For `fact(4)` the calls go down, 4 → 3 → 2 → 1 → 0, each waiting on the **call stack**; then they return up: 1, 1, 2, 6, 24. Each pending call holds its own copy of `n` and its return address. Depth n therefore uses O(n) stack space.

::: caution Typical failures
Missing or unreachable base case (infinite recursion → stack overflow); a recursive call that does not shrink the problem; recomputing the same subproblem exponentially often (naive Fibonacci).
:::

## 6.2 Programs: factorial, Fibonacci, GCD, power, binary search

```c
#include <stdio.h>

long fact(int n)            { return n <= 1 ? 1 : n * fact(n - 1); }
long gcd(long a, long b)    { return b == 0 ? a : gcd(b, a % b); }
long power(long x, int n)   {                      /* fast exponentiation, O(log n) */
    if (n == 0) return 1;
    long h = power(x, n / 2);
    return n % 2 ? h * h * x : h * h;
}
long calls = 0;
long fib(int n)             { calls++; return n < 2 ? n : fib(n - 1) + fib(n - 2); }
long fib_iter(int n)        { long a = 0, b = 1; for (int i = 0; i < n; i++) { long t = a + b; a = b; b = t; } return a; }

int bsearch_rec(const int a[], int lo, int hi, int key) {
    if (lo > hi) return -1;
    int mid = (lo + hi) / 2;
    if (a[mid] == key) return mid;
    return a[mid] < key ? bsearch_rec(a, mid + 1, hi, key) : bsearch_rec(a, lo, mid - 1, key);
}

int main(void) {
    printf("5! = %ld, 10! = %ld\n", fact(5), fact(10));
    printf("gcd(48, 18) = %ld, gcd(17, 5) = %ld\n", gcd(48, 18), gcd(17, 5));
    printf("2^10 = %ld, 3^13 = %ld\n", power(2, 10), power(3, 13));
    calls = 0; long f = fib(20);
    printf("fib(20) = %ld using %ld recursive calls; iterative gives %ld\n", f, calls, fib_iter(20));
    int a[] = {3, 8, 15, 21, 34, 55, 89};
    printf("search 34 -> %d, search 40 -> %d\n", bsearch_rec(a, 0, 6, 34), bsearch_rec(a, 0, 6, 40));
    return 0;
}
```
```output
5! = 120, 10! = 3628800
gcd(48, 18) = 6, gcd(17, 5) = 1
2^10 = 1024, 3^13 = 1594323
fib(20) = 6765 using 21891 recursive calls; iterative gives 6765
search 34 -> 4, search 40 -> -1
```

The call count shows why naive recursion can be disastrous: `fib(n)` makes 2·F(n+1) − 1 calls, which grows like 1.618ⁿ, while the loop makes n additions. Memoisation (storing results) or iteration fixes it.

## 6.3 Towers of Hanoi

Move *n* disks from peg A to peg C using peg B, one disk at a time, never placing a larger disk on a smaller one. **Recursive idea:** move the top n − 1 disks to B; move the largest to C; move the n − 1 disks from B onto C. The number of moves satisfies T(n) = 2T(n − 1) + 1, T(1) = 1, giving **T(n) = 2ⁿ − 1**. Hence 3 disks need 7 moves, 10 need 1,023, and 64 need about 1.8 × 10¹⁹.

```c
#include <stdio.h>

static int moves = 0;
void hanoi(int n, char from, char to, char via) {
    if (n == 0) return;
    hanoi(n - 1, from, via, to);
    printf("  move disk %d: %c -> %c\n", n, from, to);
    moves++;
    hanoi(n - 1, via, to, from);
}

int main(void) {
    printf("Towers of Hanoi, 3 disks:\n");
    hanoi(3, 'A', 'C', 'B');
    printf("total moves = %d (2^3 - 1)\n", moves);
    return 0;
}
```
```output
Towers of Hanoi, 3 disks:
  move disk 1: A -> C
  move disk 2: A -> B
  move disk 1: C -> B
  move disk 3: A -> C
  move disk 1: B -> A
  move disk 2: B -> C
  move disk 1: A -> C
total moves = 7 (2^3 - 1)
```

## 6.4 Recursion versus iteration

| | Recursion | Iteration |
|---|---|---|
| Mechanism | function calls + call stack | loop |
| Code | short, mirrors the definition | longer, explicit state |
| Time/space | call overhead; O(depth) stack | usually faster, O(1) extra space |
| Best for | trees, graphs, divide and conquer, backtracking | simple counting and accumulation |
| Risk | stack overflow, repeated work | none of those |

**Tail recursion** (the recursive call is the last action) can be turned into a loop mechanically, and some compilers do it. Any recursive algorithm can be written iteratively with an explicit stack.

## 6.5 Applications and the search tree: backtracking

Recursion applies wherever a problem contains smaller copies of itself: tree traversals, merge and quick sort, DFS, permutations, maze solving, parsing, directory listings. **Backtracking** builds a solution one choice at a time; whenever a partial choice cannot lead to a solution it *backs up* and tries the next option. The choices form a **search tree**; pruning bad branches early saves enormous work.

**N-queens.** Place n queens on an n × n board with none attacking another. Place one per row; for each row try each column; if the square is attacked, skip it; if no column works, return to the previous row.

```c
#include <stdio.h>
#include <stdlib.h>

int col[10], n, count, shown;

int safe(int r, int c) {
    for (int i = 0; i < r; i++)
        if (col[i] == c || abs(col[i] - c) == r - i) return 0;
    return 1;
}
void place(int r) {
    if (r == n) {
        count++;
        if (!shown && n == 4) {
            shown = 1;
            for (int i = 0; i < n; i++) { for (int j = 0; j < n; j++) putchar(col[i] == j ? 'Q' : '.'); putchar('\n'); }
        }
        return;
    }
    for (int c = 0; c < n; c++)
        if (safe(r, c)) { col[r] = c; place(r + 1); }     /* pruning: unsafe squares are never expanded */
}

int main(void) {
    int sizes[] = {4, 6, 8};
    for (int k = 0; k < 3; k++) {
        n = sizes[k]; count = 0; shown = 0;
        place(0);
        printf("%d-queens: %d solutions\n", n, count);
    }
    return 0;
}
```
```output
.Q..
...Q
Q...
..Q.
4-queens: 2 solutions
6-queens: 4 solutions
8-queens: 92 solutions
```

## 6.6 Seeing the ideas: recursion in objects, calls and trees

Recursion means defining something in terms of a smaller copy of itself. A set of Russian dolls is the usual picture: to open the doll you open the next smaller doll, and so on until the smallest doll cannot be opened. This smallest case is the **base case**, and the rule "do the same on the smaller problem" is the **recursive case**. The photographs and figures below show recursion in a puzzle, in nature, in the call stack and in a tree of calls.

```photogrid label="6.1" cols="2" ratio="1.2" caption="Recursion in a toy and in a shell. (a) A Tower of Hanoi puzzle with seven discs on three pegs; to move n discs, move n - 1 discs aside, move the largest disc, then move the n - 1 discs on top of it; this is a recursive solution. (b) A cross-section of a nautilus shell: each chamber is a scaled copy of the one before it, a self-similar spiral (the shape is a logarithmic spiral, which is often loosely, and not quite correctly, linked with Fibonacci numbers)."
@ photo id="bca201/hanoi" cap="Tower of Hanoi puzzle"
fit 1.2
focus 0.4 0.5
call 0.5 0.25 0.04 0.9 "peg A: all discs"
@ photo id="bca201/nautilus" cap="Nautilus shell cross-section"
fit 1.2
focus 0.45 0.55
```

```svgfig label="6.1" caption="The call stack of factorial(4) = 4 * factorial(3). Each call waits for the call below it, so the stack grows until the base case factorial(1) returns 1 (winding). Then each waiting call multiplies and returns (unwinding): 1, then 2 * 1 = 2, then 3 * 2 = 6, then 4 * 6 = 24. Five frames would be needed for factorial(5), so the stack depth is n, and the space cost is O(n). A missing base case would make the frames pile up until a stack overflow."
f = Fig(580, 230)
f.text(145, 14, "winding (calls)", size=10.5, color=NAVY, bold=True)
for i, n in enumerate([4, 3, 2, 1]):
    f.box(30, 28 + i * 44, 230, 36, "factorial(%d) waits for factorial(%d)" % (n, n - 1) if n > 1 else "factorial(1) returns 1", fill=BLUE if n > 1 else MINT, stroke=NAVY if n > 1 else TEAL, size=10.5, bold=True, r=0)
f.arrow([(275, 46), (275, 160)], color=NAVY, sw=1.6)
f.text(435, 14, "unwinding (returns)", size=10.5, color=TEAL, bold=True)
for i, (n, v) in enumerate([(1, "1"), (2, "2 * 1 = 2"), (3, "3 * 2 = 6"), (4, "4 * 6 = 24")]):
    f.box(330, 172 - i * 44, 230, 36, "factorial(%d) returns %s" % (n, v), fill=SAND if n < 4 else MINT, stroke=AMBER if n < 4 else TEAL, size=10.5, bold=True, r=0)
f.arrow([(315, 190), (315, 56)], color=TEAL, sw=1.6)
```

```svgfig label="6.2" caption="The tree of calls for fib(5), where fib(n) = fib(n - 1) + fib(n - 2) with fib(0) = 0 and fib(1) = 1. Notice that fib(3) is computed twice and fib(2) three times: the same work is repeated. The tree has 15 calls in all for n = 5 (the numbers of calls for n = 0 to 5 are 1, 1, 3, 5, 9, 15) and the count roughly multiplies by 1.6 for each increase of n, so the time is exponential. An iterative version, or remembering earlier values, needs only n steps."
f = Fig(580, 300)
def nd(x, y, s, fl=BLUE, st=NAVY):
    f.circle(x, y, 17, fill=fl, stroke=st, label=s, size=9.5)
pos = {}
def build(n, x, y, dx, tag=""):
    nd(x, y, "f%d" % n, fl=MINT if n < 2 else (ROSE if n == 3 or n == 2 else BLUE), st=TEAL if n < 2 else (RED if n in (2, 3) else NAVY))
    if n >= 2:
        for k, m in enumerate([n - 1, n - 2]):
            cx = x + (-dx if k == 0 else dx)
            f.line(x, y + 17, cx, y + 53 - 17, color=SLATE, sw=1.2)
            build(m, cx, y + 53, dx / 2)
build(5, 290, 24, 130)
f.text(10, 286, "pink nodes: the repeated work (f3 twice, f2 three times)", size=10, color=RED, bold=True, anchor="start")
f.text(570, 286, "15 calls for n = 5", size=10, color=NAVY, bold=True, anchor="end")
```

```svgfig label="6.3" caption="Towers of Hanoi for n = 3 discs from peg A to peg C using peg B as the spare. The recursive rule is hanoi(n, A, C, B): move n - 1 discs from A to B, move disc n from A to C, then move n - 1 discs from B to C. The seven moves are A to C, A to B, C to B, A to C, B to A, B to C, A to C. The number of moves is 2 to the power n minus 1: 1, 3, 7, 15, 31 for n = 1 to 5, and 18,446,744,073,709,551,615 for the legendary 64 discs, which at one move per second would take about 585 billion years."
f = Fig(580, 190)
moves = [("1", "A", "C"), ("2", "A", "B"), ("3", "C", "B"), ("4", "A", "C"), ("5", "B", "A"), ("6", "B", "C"), ("7", "A", "C")]
for i, (k, a, b) in enumerate(moves):
    x = 10 + i * 80
    f.box(x, 14, 74, 50, "move %s\n%s to %s" % (k, a, b), fill=BLUE if i != 3 else SAND, stroke=NAVY if i != 3 else AMBER, size=10.5, bold=True)
f.text(290, 88, "move 4 is the largest disc A to C: before it, 2 discs were parked on B", size=10, color=AMBER, bold=True)
for i, n in enumerate([1, 2, 3, 4, 5]):
    x = 10 + i * 112
    f.box(x, 108, 104, 40, "n = %d\n%d moves" % (n, 2 ** n - 1), fill=MINT, stroke=TEAL, size=10.5, bold=True)
f.text(290, 175, "moves(n) = 2 * moves(n - 1) + 1 = 2^n - 1: every extra disc doubles the work", size=10.5, color=RED, bold=True)
```

### 6.6.1 Eight applications of recursion

1. **Mathematical functions.** Factorial, power, greatest common divisor and Fibonacci numbers have natural recursive definitions that translate directly into C. Euclid's rule `gcd(a, b) = gcd(b, a % b)` is only three lines. The code reads like the definition itself.
2. **Divide and conquer sorting.** Merge sort and quick sort split the array, sort each part by calling themselves, and combine the results (Unit 8). Their speed of O(n log n) comes from this halving. Large sorting jobs, such as sorting all voter records of a district, use this approach.
3. **Binary search.** Searching a sorted array by comparing with the middle item and repeating on one half is recursive. Each call halves the problem, so 1,000,000 items need at most 20 calls. The idea is the same as finding a name in a telephone directory.
4. **Tree and graph traversal.** The traversals of a binary tree (inorder, preorder, postorder) are shortest when written recursively, because a subtree is itself a tree (Unit 7). Depth-first search of a graph is also recursive. File-system searches that visit every folder under a directory work the same way.
5. **Towers of Hanoi and puzzles.** The Hanoi solution needs no loop at all, only the three recursive steps of Figure 6.3. Other puzzles, such as mazes and the eight queens problem, use recursion with backtracking. The method tries a choice, goes deeper and returns when stuck.
6. **Parsing and compilers.** A compiler reads an expression like `(a + (b * c))` by recursive rules because brackets can be nested to any depth. The same idea reads HTML pages and JSON files, which nest inside themselves. This is how a browser builds the page you see from the Nagarik App site.
7. **Fractals and graphics.** Snowflakes, trees and coastlines are drawn by calling a drawing function on smaller copies of the shape. The nautilus shell of Plate 6.1 is a natural example of self-similarity. Computer graphics use this to make realistic scenery with very little code.
8. **Combinatorial problems.** Generating all permutations or subsets of a set, and counting the paths in a grid, are recursive tasks. The recursion tree lists every possibility in an orderly way. Test-case generators and route planners use this idea.

## Formula and fact sheet

- Recursive definition = base case + smaller recursive case.
- n! = n·(n−1)!; gcd(a, b) = gcd(b, a mod b); Fibonacci F(n) = F(n−1) + F(n−2).
- Hanoi: T(n) = 2ⁿ − 1 moves. Naive Fibonacci: exponential, about 1.618ⁿ calls.
- Recursion depth d costs O(d) stack space.
- Binary search: T(n) = T(n/2) + 1 → O(log n).

## Chapter summary

- Recursion solves a problem through smaller versions of itself and needs a reachable base case.
- The call stack stores pending calls; deep or repeated recursion costs memory and time.
- Hanoi needs 2ⁿ − 1 moves; naive Fibonacci recomputes subproblems; iteration or memoisation removes the waste.
- Backtracking explores a search tree and prunes dead branches (N-queens).

## Practice

1. Define recursion; what are the base case and recursive case of `sum(n) = 1 + 2 + … + n`?
2. Trace `fact(4)` showing the call stack.
3. Write a recursive function to compute the sum of digits of an integer; trace it for 4,725.
4. How many moves does Hanoi need for 5 disks? Derive the recurrence.
5. Trace `gcd(252, 105)`.
6. Distinguish recursion from iteration and say when each is better.
7. Why is `fib(40)` slow in the naive version? Suggest two fixes.
8. What happens if the base case is missing?
9. Explain how backtracking prunes the 4-queens search tree.

::: note Answers and worked solutions
**1.** Recursion = a function that calls itself on a smaller problem. Base case: `sum(0) = 0` (or `sum(1) = 1`). Recursive case: `sum(n) = n + sum(n − 1)`.
**2.** fact(4) → 4·fact(3) → 3·fact(2) → 2·fact(1) → returns 1; unwinding: 2·1 = 2, 3·2 = 6, 4·6 = 24. The stack holds four pending frames at its deepest.
**3.** `int ds(int n){ return n == 0 ? 0 : n % 10 + ds(n / 10); }` ds(4725) = 5 + ds(472) = 5 + 2 + ds(47) = 5 + 2 + 7 + ds(4) = 5 + 2 + 7 + 4 + 0 = **18**.
**4.** T(n) = 2T(n−1) + 1 with T(1) = 1 → 2ⁿ − 1; for n = 5: **31** moves.
**5.** gcd(252, 105) → gcd(105, 42) → gcd(42, 21) → gcd(21, 0) = **21**.
**6.** See the table in 6.4: use recursion for self-similar structures (trees, divide and conquer), iteration for simple loops where speed and memory matter.
**7.** It recomputes the same values exponentially often (about 3.3 × 10⁸ calls for n = 40). Fixes: iteration (O(n)); memoisation (store computed values in an array).
**8.** The calls never stop; the stack fills and the program crashes with stack overflow.
**9.** After placing a queen in row 0, any square attacked in later rows is skipped; if a row has no safe column the search returns to the previous row immediately, so entire subtrees of impossible placements are never generated.
:::

## Model answers (5 and 10 marks)

**Q1. What is recursion? Explain base case and recursive case with the factorial function and trace factorial(4). (5 marks)**

**Recursion** is a technique in which a function calls itself to solve a smaller instance of the same problem. A correct recursive function has two parts.

1. **Base case:** the simplest instance, which is answered directly without a further call. It stops the recursion.
2. **Recursive case:** the rule that reduces the problem and calls the function again on a smaller input, moving towards the base case.

```c
long factorial(int n) {
    if (n <= 1) return 1;          /* base case */
    return n * factorial(n - 1);   /* recursive case */
}
```

**Trace of factorial(4) (Figure 6.1).** The call `factorial(4)` waits for `factorial(3)`, which waits for `factorial(2)`, which waits for `factorial(1)`. The base case returns 1. Then the calls return in reverse order: `factorial(2)` returns 2 * 1 = 2, `factorial(3)` returns 3 * 2 = 6 and `factorial(4)` returns 4 * 6 = **24**. Four stack frames exist at the deepest point, so space is O(n); the time is O(n) because there are n calls. If the base case were missing, the calls would never stop and the program would crash with a stack overflow.

**Q2. Compare recursion and iteration. (5 marks)**

**Recursion** repeats work by a function calling itself; **iteration** repeats work by a loop (`for`, `while`). Any recursive function can be written with a loop and a stack, and many loops can be written recursively.

| Point | Recursion | Iteration |
|---|---|---|
| Mechanism | function calls itself | loop repeats a block |
| Termination | base case reached | loop condition becomes false |
| Memory | one stack frame per call, O(n) | constant, O(1) |
| Speed | slower because of call overhead | usually faster |
| Code | short, close to the definition | longer, but simple |
| Risk | stack overflow, repeated work (naive Fibonacci) | infinite loop |
| Best for | trees, divide and conquer, backtracking | simple counting and summation |

For example, factorial with a loop uses one variable and no extra frames, while the naive recursive Fibonacci makes 15 calls for n = 5 because it repeats work (Figure 6.2); an iterative version needs only 5 steps. Recursion is preferred when the problem is itself recursive, such as tree traversal or Towers of Hanoi, because the code is clear and short. Iteration is preferred when speed and memory matter.

**Q3. Explain the Towers of Hanoi problem. Write the recursive algorithm, trace it for 3 discs and derive the number of moves. (10 marks)**

**Problem.** Three pegs A, B and C are given. Peg A holds n discs of different sizes, the largest at the bottom. All discs must be moved to peg C, one disc at a time, using B as a spare, and a larger disc may never be placed on a smaller one (Plate 6.1a).

**Recursive idea.** To move n discs from the source to the target: (1) move the top n - 1 discs from source to the spare peg; (2) move the largest disc from source to target; (3) move the n - 1 discs from the spare peg to the target. The base case is n = 1, a single move.

```c
void hanoi(int n, char from, char to, char via) {
    if (n == 1) { printf("move 1 from %c to %c\n", from, to); return; }
    hanoi(n - 1, from, via, to);
    printf("move %d from %c to %c\n", n, from, to);
    hanoi(n - 1, via, to, from);
}
```

**Trace for n = 3 (Figure 6.3).** `hanoi(3, A, C, B)` first calls `hanoi(2, A, B, C)`, which gives: disc 1 A to C, disc 2 A to B, disc 1 C to B. Then disc 3 moves A to C. Finally `hanoi(2, B, C, A)` gives: disc 1 B to A, disc 2 B to C, disc 1 A to C. The total is seven moves: A-C, A-B, C-B, A-C, B-A, B-C, A-C.

**Number of moves.** Let M(n) be the moves for n discs. Then M(1) = 1 and M(n) = M(n - 1) + 1 + M(n - 1) = 2 M(n - 1) + 1. Solving gives **M(n) = 2 to the power n minus 1**.

| n | 1 | 2 | 3 | 4 | 5 | 10 | 64 |
|---|---|---|---|---|---|---|---|
| Moves | 1 | 3 | 7 | 15 | 31 | 1,023 | 18,446,744,073,709,551,615 |

**Complexity.** Time is O(2 to the power n), exponential: every extra disc doubles the work. Space is O(n) for the call stack, because the depth of recursion is n. For 64 discs at one move per second the work would take about 585 billion years, so the problem is a standard example of an algorithm that is simple to write but impossible to run for large n.

**Conclusion.** Hanoi shows the strength of recursion: the three-step idea solves any n with five lines of code, whereas an iterative solution is much harder to write correctly.
