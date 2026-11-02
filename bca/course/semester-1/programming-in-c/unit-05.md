---
subject: Programming in C
grade: BCA Semester 1
unit: 5
title: Functions, Recursion and Storage Classes
hours: 6
area: BCA 102 · Programming in C · Unit 6
---

A function is a named block of code that does one job. Functions let you split a large program into pieces you can write, test and reuse separately. Everything in C other than `main` is a function, and `printf` is simply a function someone else wrote.

::: key What this unit gives you
- Declaration (prototype), definition and call; return values; `void`.
- Call by value, and how arrays behave differently.
- Recursion: base case, recursive case, call stack, and when not to use it.
- Scope and the four storage classes `auto`, `static`, `extern`, `register`.
:::

## 5.1 Defining and calling

```text
return_type name(parameter_list)
{
    body
    return value;
}
```

- **Prototype (declaration)**: `int add(int a, int b);` tells the compiler the name, parameter types and return type so it can check calls that appear *before* the definition. Put prototypes at the top of the file or in a header.
- **Definition**: the body.
- **Call**: `s = add(3, 4);`. The values 3 and 4 are the **actual arguments**; `a` and `b` are the **formal parameters**.
- A function with no result has return type `void`; one with no parameters is written `(void)`. A non-`void` function must `return` a value on every path, and `return` ends the function at once.

```c
#include <stdio.h>

long long factorial(int n);
int gcd(int a, int b);
int is_prime(int n);

int main(void)
{
    printf("%lld %d %d %d\n", factorial(15), gcd(84, 36), is_prime(97), is_prime(91));
    return 0;
}

long long factorial(int n)
{
    long long f = 1;
    for (int i = 2; i <= n; i++)
        f *= i;
    return f;
}

int gcd(int a, int b)
{
    while (b != 0) {
        int r = a % b;
        a = b;
        b = r;
    }
    return a;
}

int is_prime(int n)
{
    if (n < 2) return 0;
    for (int i = 2; i * i <= n; i++)
        if (n % i == 0) return 0;
    return 1;
}
```
```output
1307674368000 12 1 0
```

(91 = 7 × 13, so `is_prime(91)` is 0.)

## 5.2 Parameter passing

C passes **by value**: the function receives a *copy* of each argument. Changing the parameter never changes the caller's variable, which is why a naive `swap(a, b)` fails.

```c
#include <stdio.h>

void swap_wrong(int a, int b) { int t = a; a = b; b = t; }
void swap_right(int *a, int *b) { int t = *a; *a = *b; *b = t; }

void double_all(int arr[], int n)
{
    for (int i = 0; i < n; i++)
        arr[i] *= 2;
}

int main(void)
{
    int x = 1, y = 2;
    swap_wrong(x, y);
    printf("after wrong: %d %d\n", x, y);
    swap_right(&x, &y);
    printf("after right: %d %d\n", x, y);
    int v[3] = {1, 2, 3};
    double_all(v, 3);
    printf("array: %d %d %d\n", v[0], v[1], v[2]);
    return 0;
}
```
```output
after wrong: 1 2
after right: 2 1
array: 2 4 6
```

To let a function change a caller's variable, pass its **address** (a pointer; Unit 6) – this is "call by reference" simulated in C. **Arrays** are special: an array name used as an argument becomes the address of its first element, so the function works on the *original* array. That is why `double_all` changed `v`, and why the function needs the length as a separate parameter: inside the function `sizeof(arr)` is the size of a pointer, not the array.

A function returns only one value. To return several, use pointer parameters or a structure.

## 5.3 Recursion

A function that calls itself is **recursive**. Every correct recursive function has

1. a **base case** that stops the recursion without another call, and
2. a **recursive case** that moves *towards* the base case.

Each call gets its own frame on the **call stack** holding its parameters, locals and return address; frames are popped as calls return.

```c
#include <stdio.h>

int fact(int n)            { return n <= 1 ? 1 : n * fact(n - 1); }
int fib(int n)             { return n < 2 ? n : fib(n - 1) + fib(n - 2); }
int sum_digits(int n)      { return n == 0 ? 0 : n % 10 + sum_digits(n / 10); }
int power(int b, int e)    { return e == 0 ? 1 : b * power(b, e - 1); }
void hanoi(int n, char from, char to, char via, int *moves)
{
    if (n == 0) return;
    hanoi(n - 1, from, via, to, moves);
    (*moves)++;
    if (n == 3) printf("move disk 3 from %c to %c\n", from, to);
    hanoi(n - 1, via, to, from, moves);
}

int main(void)
{
    printf("%d %d %d %d\n", fact(6), fib(10), sum_digits(4305), power(2, 10));
    int moves = 0;
    hanoi(4, 'A', 'C', 'B', &moves);
    printf("moves for 4 disks: %d\n", moves);
    return 0;
}
```
```output
720 55 12 1024
move disk 3 from A to B
move disk 3 from B to C
moves for 4 disks: 15
```

Trace `fact(3)`: `fact(3)` → `3 * fact(2)` → `2 * fact(1)` → `fact(1)` returns 1 → returns 2 → returns 6. The Tower of Hanoi needs 2ⁿ − 1 moves (15 for n = 4).

**Cost of recursion.** `fib(n)` as written recomputes the same values and takes about 1.6ⁿ calls (exponential); an iterative loop takes n steps. Recursion also costs stack memory, and a missing base case ends in a *stack overflow*. Use recursion when the problem is naturally self-similar (trees, divide-and-conquer, Hanoi, permutations); use loops for simple counting.

**Recursion vs iteration.** Recursion: shorter and clearer for self-similar problems, slower and more memory-hungry. Iteration: faster and constant memory, sometimes clumsier.

## 5.4 Scope and storage classes

**Scope** is where a name can be used. A *local* variable lives in a block `{ }` and is created on entry and destroyed on exit; a *global* variable is declared outside every function and is visible to all functions below it. An inner declaration **shadows** an outer one of the same name. Prefer locals and parameters: globals make code hard to reason about.

| Class | Where stored | Default value | Lifetime | Scope |
|---|---|---|---|---|
| `auto` (default for locals) | stack | garbage | the block | the block |
| `register` | CPU register if available (a request only; you cannot take its address) | garbage | the block | the block |
| `static` (local) | static data area | **0** | whole program | the block, but the value **persists** between calls |
| `static` (global) | static data area | 0 | whole program | this file only |
| `extern` | static data area | 0 | whole program | declares a global defined in another file |

```c
#include <stdio.h>

int counter(void)
{
    static int calls = 0;
    int fresh = 0;
    calls++;
    fresh++;
    return calls * 10 + fresh;
}

int g = 100;

int main(void)
{
    int r1 = counter();
    int r2 = counter();
    int r3 = counter();
    printf("%d %d %d\n", r1, r2, r3);
    int g = 5;
    printf("%d\n", g);
    {
        int g = 7;
        printf("%d\n", g);
    }
    return 0;
}
```
```output
11 21 31
5
7
```

`calls` keeps its value (1, 2, 3), `fresh` is rebuilt every call. The three calls are made in separate statements on purpose: the order in which the arguments of one `printf(…)` are evaluated is **unspecified** in C (GCC happens to go right to left), so `printf("%d %d", counter(), counter())` has no guaranteed output. `main`'s local `g` shadows the global `g = 100`.

**Header files and the `main` arguments.** A header holds prototypes and macros; `#include "mine.h"` (quotes) searches your folder first, `#include <stdio.h>` searches system folders. `int main(int argc, char *argv[])` receives the command line: `argc` is the number of words and `argv[0]` is the program name.

## Formula and fact sheet

- Prototype before use; definition has a body; actual vs formal arguments.
- C is **call by value**; pass `&x` to modify `x`; arrays are passed as addresses.
- Recursion = base case + progress towards it; Hanoi = 2ⁿ − 1 moves; naive Fibonacci is exponential.
- `static` local keeps its value; `auto` locals are garbage until set; globals default to 0.

## Chapter summary

- Write small functions with one purpose and a prototype.
- Remember copies are passed; use pointers for output parameters.
- Recursion needs a base case; know the cost.
- Know where each variable lives and how long it lasts.

## Practice

**A. Short questions**

1. Differentiate a function declaration from a definition. Why do we need a prototype?
2. Explain why `swap(int a, int b)` cannot swap the caller's variables.
3. What happens if a recursive function has no base case?
4. Distinguish `auto`, `static` and `extern` by lifetime and visibility.
5. Why is `sizeof(arr)` inside a function that receives `int arr[]` not the array size?

**B. Predict the output**

6. `int f(int n){ return n == 0 ? 0 : n + f(n - 1); }` → `printf("%d", f(5));`
7. `void g(void){ static int c = 0; c += 2; printf("%d ", c); }` called three times in `main`.
8. `int a = 5; { int a = 10; } printf("%d", a);`

**C. Programs**

9. Write a recursive function for the sum of the first n natural numbers and one for the nth term of Fibonacci; compare the speed idea.
10. Write `int power(int base, int exp)` using fast exponentiation (squaring) and state its number of multiplications for exp = 16.
11. Write a recursive binary-search function.
12. Write a function that returns both the minimum and the maximum of an array.

::: note Answers and worked solutions
**1.** A declaration states the name and types; a definition provides the body. The prototype lets the compiler check argument count and types of calls that appear before the definition.
**2.** The function swaps its own copies; the originals are untouched. Pass addresses and swap `*a` and `*b`.
**3.** Calls never stop; each pushes a stack frame, and the program crashes with a stack overflow.
**4.** `auto`: stack, lasts for the block. `static`: lasts for the program; for locals it keeps its value between calls. `extern`: refers to a global defined elsewhere.
**5.** The array decays to a pointer, so `sizeof` returns the size of a pointer (typically 8), not n × sizeof(int).
**6.** 5 + 4 + 3 + 2 + 1 + 0 = 15.
**7.** `2 4 6`.
**8.** 5 (the inner `a` ended with its block).
**9.** `int sum(int n){ return n == 0 ? 0 : n + sum(n - 1); }`. Simple recursive Fibonacci takes exponentially many calls; the loop version takes n steps.
**10.** `int power(int b, int e){ if (e == 0) return 1; int h = power(b, e / 2); return e % 2 ? h * h * b : h * h; }` For exp = 16 it needs 4 squarings plus the base case (versus 15 multiplications naively).
**11.** `int bs(int a[], int lo, int hi, int k){ if (lo > hi) return -1; int m = lo + (hi - lo) / 2; if (a[m] == k) return m; return a[m] < k ? bs(a, m + 1, hi, k) : bs(a, lo, m - 1, k); }`
**12.** `void minmax(int a[], int n, int *mn, int *mx){ *mn = *mx = a[0]; for (int i = 1; i < n; i++){ if (a[i] < *mn) *mn = a[i]; if (a[i] > *mx) *mx = a[i]; } }`
:::
