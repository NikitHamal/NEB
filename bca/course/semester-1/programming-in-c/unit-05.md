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

```svgfig label="5.1" caption="The call stack while factorial(3) runs. Each call pushes a new frame holding its own n; the calls wait for each other until n = 1 is reached, then the answers return in reverse order: 1, 2, 6."
f = Fig(760, 270)
frames = [("main()", "calls factorial(3)"), ("factorial(3)", "n = 3, waits for 3 * factorial(2)"), ("factorial(2)", "n = 2, waits for 2 * factorial(1)"), ("factorial(1)", "n = 1, base case: returns 1")]
for i, (a, b) in enumerate(frames):
    y = 214 - i * 52
    f.box(30, y, 300, 44, "", fill=BLUE if i < 3 else SOFT, stroke=NAVY)
    f.text(46, y + 19, a, size=11.5, color=NAVY, bold=True, anchor="start")
    f.text(46, y + 36, b, size=10, color=SLATE, anchor="start")
f.arrow([(350, 236), (350, 30)], color=AMBER, label="stack grows", lpos=(398, 130))
f.text(560, 40, "Returning", size=11.5, color=TEAL, bold=True)
for i, s in enumerate(["factorial(1) returns 1", "factorial(2) returns 2 * 1 = 2", "factorial(3) returns 3 * 2 = 6", "main prints 6"]):
    f.text(470, 70 + i * 34, f"{i + 1}.  {s}", size=11, color=NAVY, anchor="start")
f.text(470, 224, "Without a base case the stack overflows.", size=10.5, color=RED, bold=True, anchor="start")
```

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

```svgfig label="5.2" caption="Where the four storage classes live. Local (auto) variables sit on the stack and vanish when the function returns; static and global variables live for the whole run in the data segment; register asks for a CPU register."
f = Fig(760, 260)
segs = [("Code (text)", "machine instructions", SOFT), ("Data segment", "global and static variables", BLUE), ("Heap", "malloc / calloc memory, grows up", SOFT), ("free space", "", "#ffffff"), ("Stack", "auto variables, parameters, grows down", BLUE)]
for i, (a, b, c) in enumerate(segs):
    y = 10 + i * 46
    f.box(30, y, 270, 42, "", fill=c, stroke=NAVY)
    f.text(165, y + 19, a, size=11.5, color=NAVY, bold=True)
    if b: f.text(165, y + 35, b, size=9.5, color=SLATE)
rows = [("auto", "block", "stack", "garbage"), ("static", "block / file", "data", "0"), ("extern", "program", "data", "0"), ("register", "block", "CPU register", "garbage")]
f.text(330, 22, "class", size=10.5, color=TEAL, bold=True, anchor="start"); f.text(410, 22, "scope", size=10.5, color=TEAL, bold=True, anchor="start"); f.text(520, 22, "stored in", size=10.5, color=TEAL, bold=True, anchor="start"); f.text(650, 22, "default", size=10.5, color=TEAL, bold=True, anchor="start")
for i, r in enumerate(rows):
    for j, x in enumerate((330, 410, 520, 650)):
        f.text(x, 52 + i * 30, r[j], size=10.5, color=NAVY if j == 0 else SLATE, bold=(j == 0), anchor="start")
f.text(330, 200, "Lifetime: auto = one call; static, extern = whole program.", size=10.5, color=SLATE, anchor="start")
```

## 5.5 Eight advantages of using functions

1. **Divide and conquer.** A big problem is split into small tasks, each written as a function such as `read_marks()` or `find_grade()`. Each function can be understood by itself. A team of four students can then write four functions in parallel.
2. **Reusability.** A function is written once and called many times, with different arguments. `power(base, exp)` can serve a loan calculator and a physics program alike. This saves typing and reduces mistakes.
3. **Easy testing and debugging.** Each function can be tested alone with a few known inputs. When the total is wrong, the programmer checks only the `total()` function. This is much faster than reading a 500-line `main`.
4. **Shorter, clearer `main`.** `main` becomes a short list of calls that reads like a plan of the program. A reader sees at once what happens in what order. The details stay hidden inside the functions.
5. **Easy maintenance.** If the VAT rate in Nepal changes, only the function `vat()` is edited, and all bills follow the new rule. Without functions the same rate would be hunted in many places. Maintenance cost is a big part of software cost.
6. **Library building.** Functions can be collected in header and object files and shared between programs, as the C library itself does with `printf` and `sqrt`. A college can keep its own `student.h`. Code grows into a library instead of being copied.
7. **Recursion.** A function that calls itself solves problems with a self-similar structure, such as factorial, Fibonacci, the Tower of Hanoi and tree traversal. The code is short and close to the mathematical definition. It needs a base case and uses stack memory for every call.
8. **Data protection through scope.** Local variables exist only inside their function, so two functions can both use a variable named `i` without conflict. Only the values passed as arguments cross the boundary. This lowers the chance of one part of the program damaging another.

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

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Differentiate call by value and call by reference (address). Write a program that shows that a swap function needs addresses.**

In **call by value** the function receives a *copy* of each argument. Changes made to the parameters affect only the copy, so the caller's variables stay unchanged. In **call by reference** (in C, done by passing the *address* with `&` and receiving it in a pointer parameter) the function works on the original memory through `*p`, so changes are visible to the caller. C itself always passes by value; "by reference" is imitated by passing a pointer.

| Point | Call by value | Call by address |
|---|---|---|
| What is passed | copy of the value | address of the variable |
| Original changed? | no | yes |
| Call | `swap(x, y)` | `swap(&x, &y)` |
| Parameter | `int a` | `int *a` |
| Use | read-only inputs | results, arrays, large structures |

```c
#include <stdio.h>
void swap_val(int a, int b) { int t = a; a = b; b = t; }
void swap_ref(int *a, int *b) { int t = *a; *a = *b; *b = t; }
int main(void) {
    int x = 10, y = 20;
    swap_val(x, y);
    printf("after call by value:   x=%d y=%d\n", x, y);
    swap_ref(&x, &y);
    printf("after call by address: x=%d y=%d\n", x, y);
    return 0;
}
```

```text
after call by value:   x=10 y=20
after call by address: x=20 y=10
```

`swap_val` swapped only its own copies, which disappeared when it returned. `swap_ref` changed the real x and y. An array is always passed by address, so a function that sorts an array changes the caller's array.

**Q (10 marks). What is recursion? Explain it with a factorial and a Fibonacci function, and show how the call stack works. Compare recursion with iteration. Also explain the four storage classes of C.**

*Introduction.* **Recursion** is a method in which a function calls itself to solve a smaller copy of the same problem. A recursive function needs (1) a **base case** that stops the calls and (2) a **recursive case** that moves toward the base case.

*Factorial.* n! = n × (n - 1)!, with 0! = 1! = 1. The function `long fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }` gives 5! = 120. For `fact(3)` the calls go down to `fact(1)`, which returns 1; then 2 × 1 = 2 and 3 × 2 = 6 come back (Figure 5.1). Each pending call keeps its own `n` in a **stack frame**.

*Fibonacci.* `int fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }` gives 0 1 1 2 3 5 8 for n = 0 to 6. It is simple, but `fib(n)` recomputes the same values many times, so the time grows roughly as 1.6ⁿ; a loop takes only n steps.

```text
5! = 120
0 1 1 2 3 5 8 
```

*Recursion versus iteration.*

| Point | Recursion | Iteration |
|---|---|---|
| Method | function calls itself | loop repeats a block |
| Termination | base case | loop condition |
| Memory | one stack frame per call | constant |
| Speed | slower (call overhead) | faster |
| Code | short, close to the definition | longer, but efficient |
| Risk | stack overflow | endless loop |

*Storage classes* decide the scope (where a name can be used), lifetime and default value (Figure 5.2).

1. **`auto`**: default for local variables; lives on the stack during one call; starts with garbage.
2. **`register`**: a request to keep the variable in a CPU register for speed; its address cannot be taken.
3. **`static`**: a local variable that keeps its value between calls and starts at 0. A function with `static int c = 0; return ++c;` called three times returns 3.
4. **`extern`**: declares a global variable defined in another place or file, so several files share one variable.

*Conclusion.* Recursion expresses self-similar problems clearly, and the stack makes it work, but every call costs memory. Use it for trees, divide and conquer and the Tower of Hanoi, and use loops when a simple loop is enough.
