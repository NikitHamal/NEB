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
