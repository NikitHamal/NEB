---
subject: Computer Science
grade: 12
unit: 4
title: Programming in C
hours: 12
---

In Grade 11 you learned to write a single `main()` that read some values, looped
over them and printed an answer. That is enough for twenty lines of code and
hopeless for two hundred. This unit adds the four tools that let a C program
grow: **functions** (break the work into named pieces), **structures and
unions** (group related data under one name), **pointers** (work with memory
addresses directly), and **files** (keep the data after the program ends).

::: key What the examiner asks from this unit
Almost every paper contains one program from this unit — a function, a recursion
(factorial or Fibonacci), an array of structures, or a file that is written and
read back. Learn the difference between **call by value and call by reference**,
between **structure and union**, and the sequence **fopen → read/write →
fclose**. Write the `#include`, the prototype and the `return 0;` — they carry
marks.
:::

## 4.1 Review of C programming concepts

C was written by Dennis Ritchie at Bell Laboratories in 1972. It is a
**structured, mid-level, compiled** language: close enough to the hardware to
write an operating system, structured enough to be readable.

```figure caption="The parts of a C program. Only main() is compulsory; everything above it prepares the compiler and everything below it is the work broken into functions."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.9, 3.2))

parts = [("Documentation", "/* purpose, author, date */", "#f4f6f9", MUTED),
         ("Preprocessor / link", "#include <stdio.h>", "#eef4fa", ACCENT),
         ("Definition", "#define PI 3.1416", "#eef4fa", ACCENT),
         ("Global declaration", "int shared;   int f(int);", "#f3eefa", "#6a5acd"),
         ("main() function", "int main() { ... return 0; }", "#eaf3ee", "#2e8b57"),
         ("User-defined functions", "int f(int n) { ... }", "#fdf3e6", "#c98a1e")]
for i, (a, b, fc, ec) in enumerate(parts):
    y = 2.72 - i*0.50
    ax.add_patch(FancyBboxPatch((0.15, y), 4.30, 0.40, boxstyle="round,pad=0.03",
                                facecolor=fc, edgecolor=ec, lw=1.1))
    ax.text(0.30, y + 0.20, a, fontsize=6.8, color=INK, va="center")
    ax.text(2.10, y + 0.20, b, fontsize=6.0, color=MUTED, va="center",
            family="monospace")
ax.annotate("", xy=(0.05, 0.22), xytext=(0.05, 3.10),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, mutation_scale=9))
ax.text(4.60, 1.60, "order\nmatters", fontsize=6.2, color=MUTED, va="center")
ax.set_xlim(-0.05, 5.4); ax.set_ylim(0.05, 3.25)
ax.axis("off")
```

```c
#include <stdio.h>
int main() {
    int roll = 12;
    float percent = 78.5f;
    char grade = 'A';
    char name[20] = "Anisha";
    printf("Roll    = %d\n", roll);
    printf("Percent = %.2f\n", percent);
    printf("Grade   = %c\n", grade);
    printf("Name    = %s\n", name);
    printf("sizes: int=%d float=%d char=%d double=%d\n",
           (int)sizeof(int), (int)sizeof(float), (int)sizeof(char), (int)sizeof(double));
    int a = 17, b = 5;
    printf("%d %d %d %d %d\n", a+b, a-b, a*b, a/b, a%b);
    return 0;
}
```

Output:

```
Roll    = 12
Percent = 78.50
Grade   = A
Name    = Anisha
sizes: int=4 float=4 char=1 double=8
22 12 85 3 2
```

Note `17 / 5` gives **3**, not 3.4: dividing one integer by another throws away
the fraction. Write `17 / 5.0` if you want 3.4.

| Item | Examples |
|---|---|
| Data types | `int`, `float`, `double`, `char`, `void`; modifiers `short`, `long`, `signed`, `unsigned` |
| Format specifiers | `%d` int, `%f` float, `%c` char, `%s` string, `%ld` long, `%p` pointer |
| Operators | `+ - * / %`, `= += -=`, `== != < >`, `&& || !`, `++ --`, `?:`, `& *` |
| Decisions | `if`, `if-else`, `if-else-if`, nested `if`, `switch-case` |
| Loops | `for`, `while`, `do-while`; `break` and `continue` |
| Arrays | `int marks[5] = {78, 52, 85, 91, 45};` — index starts at **0** |

```c
int marks[5] = {78, 52, 85, 91, 45};
int i, sum = 0, max = marks[0];
for (i = 0; i < 5; i++) {
    sum += marks[i];
    if (marks[i] > max) max = marks[i];
}
printf("sum = %d, average = %.2f, highest = %d\n", sum, sum / 5.0, max);
```

Output:

```
sum = 351, average = 70.20, highest = 91
```

## 4.2 Functions: library and user-defined; advantages

::: definition Function
A **function** is a self-contained, named block of code that performs one task,
may accept **arguments** and may **return** one value. A C program is nothing
but a collection of functions, of which `main()` is the one the system calls
first.
:::

```figure caption="Functions in C are either supplied with the compiler (library) or written by the programmer (user-defined)."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.15, 2.5))

def nb(x, y, w, t, fc, ec, fs=6.6, h=0.46):
    ax.add_patch(FancyBboxPatch((x - w/2, y - h/2), w, h, boxstyle="round,pad=0.04",
                                facecolor=fc, edgecolor=ec, lw=1.1))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs, color=INK)

def elbow(x1, y1, x2, y2):
    ym = (y1 + y2) / 2
    ax.plot([x1, x1, x2, x2], [y1, ym, ym, y2], color=MUTED, lw=0.9, zorder=0)

nb(4.0, 2.55, 2.0, "C functions", "#f4f6f9", INK, fs=7.6)
nb(1.95, 1.72, 2.0, "Library (built-in)", "#eef4fa", ACCENT, fs=7.0)
nb(6.15, 1.72, 2.0, "User-defined", "#eaf3ee", "#2e8b57", fs=7.0)
elbow(4.0, 2.32, 1.95, 1.95); elbow(4.0, 2.32, 6.15, 1.95)

for x, t in [(0.72, "stdio.h\nprintf, scanf"), (1.95, "math.h\nsqrt, pow"),
             (3.18, "string.h\nstrcpy, strlen")]:
    nb(x, 0.68, 1.06, t, "white", ACCENT, fs=5.6, h=0.60)
    elbow(1.95, 1.49, x, 0.98)
for x, t in [(5.30, "factorial()"), (6.55, "area()"), (7.70, "swap()")]:
    nb(x, 0.68, 0.98, t, "white", "#2e8b57", fs=5.9, h=0.60)
    elbow(6.15, 1.49, x, 0.98)
ax.text(1.95, 0.16, "must #include the header", ha="center", fontsize=6.0, color=ACCENT)
ax.text(6.15, 0.16, "you write the body yourself", ha="center", fontsize=6.0,
        color="#2e8b57")
ax.set_xlim(0.0, 8.35); ax.set_ylim(0.05, 2.85)
ax.axis("off")
```

| | Library function | User-defined function |
|---|---|---|
| Written by | The compiler's authors | The programmer |
| Where it lives | In a header and the standard library | In the programmer's own source file |
| Needs | `#include <stdio.h>` etc. | A definition, and usually a prototype |
| Body | Not visible; already compiled | Visible and editable |
| Examples | `printf`, `scanf`, `sqrt`, `strlen`, `getc` | `factorial`, `area`, `swap` |

**Advantages of using functions**

1. **Reusability** — write once, call as many times as needed.
2. **Modularity** — a large problem is broken into small, independent tasks.
3. **Readability** — `factorial(n)` says what it does; twelve lines of loop do not.
4. **Easier testing and debugging** — each function can be checked on its own.
5. **Shorter program** — no repeated blocks of code.
6. **Teamwork** — different people can write different functions at the same time.
7. **Easier maintenance** — a change is made in one place only.

## 4.3 Function definition, prototype, call and return

Three things must agree: the **prototype** (declaration), the **definition**
(the body) and the **call**.

```figure caption="How a function call works. Control leaves main(), the arguments are copied into the parameters, the body runs, and return sends one value back to exactly the point of the call."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(5.15, 2.8))

ax.add_patch(FancyBboxPatch((0.15, 0.70), 2.85, 1.75, boxstyle="round,pad=0.05",
                            facecolor="#eef4fa", edgecolor=ACCENT, lw=1.2))
ax.text(1.57, 2.28, "main()  — the caller", ha="center", fontsize=7.0, color=INK)
ax.text(0.32, 1.85, "int r;", fontsize=6.2, color=MUTED, family="monospace")
ax.text(0.32, 1.52, "r = factorial(5);", fontsize=6.4, color=INK, family="monospace")
ax.text(0.32, 1.08, 'printf("%d", r);', fontsize=6.2, color=MUTED, family="monospace")

ax.add_patch(FancyBboxPatch((4.90, 0.70), 3.00, 1.75, boxstyle="round,pad=0.05",
                            facecolor="#eaf3ee", edgecolor="#2e8b57", lw=1.2))
ax.text(6.40, 2.28, "factorial()  — the callee", ha="center", fontsize=7.0, color=INK)
ax.text(5.05, 1.88, "int factorial(int n) {", fontsize=6.2, color=INK,
        family="monospace")
ax.text(5.23, 1.56, "f = f * i;  ...", fontsize=6.2, color=MUTED, family="monospace")
ax.text(5.23, 1.24, "return f;", fontsize=6.4, color=INK, family="monospace")
ax.text(5.05, 0.92, "}", fontsize=6.2, color=MUTED, family="monospace")

ax.annotate("", xy=(4.85, 1.78), xytext=(3.05, 1.55),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.3, mutation_scale=11))
ax.text(3.95, 2.12, "call:\n5 copied into n",
        ha="center", va="center", fontsize=6.0, color=ACCENT)
ax.annotate("", xy=(3.05, 1.18), xytext=(4.85, 1.15),
            arrowprops=dict(arrowstyle="-|>", color="#2e8b57", lw=1.3, mutation_scale=11))
ax.text(3.95, 0.86, "return: 120 goes\nback to the call", ha="center", va="center",
        fontsize=6.0, color="#2e8b57")
ax.text(0.15, 0.36, "prototype at the top of the file:  int factorial(int n);",
        fontsize=6.4, color=MUTED, family="monospace")
ax.text(0.15, 0.12, "it tells the compiler the return type and the parameter types",
        fontsize=6.2, color=MUTED)
ax.set_xlim(0.0, 8.0); ax.set_ylim(0.0, 2.55)
ax.axis("off")
```

```c
#include <stdio.h>
#include <math.h>

/* function prototypes (declarations) */
int  factorial(int n);
float area(float l, float b);
void greet(void);

int main() {
    greet();
    printf("factorial(5) = %d\n", factorial(5));
    printf("area(8, 5)   = %.2f\n", area(8, 5));
    printf("sqrt(144)    = %.2f   pow(2,10) = %.0f\n", sqrt(144.0), pow(2, 10));
    return 0;
}

/* function definitions */
void greet(void) { printf("Namaste from a user-defined function!\n"); }

int factorial(int n) {
    int i, f = 1;
    for (i = 1; i <= n; i++) f = f * i;
    return f;                       /* return sends the value back */
}

float area(float l, float b) { return l * b; }
```

Output:

```
Namaste from a user-defined function!
factorial(5) = 120
area(8, 5)   = 40.00
sqrt(144)    = 12.00   pow(2,10) = 1024
```

- **Prototype**: `int factorial(int n);` — return type, name, parameter types, a
  semicolon. Placed before `main()` so the compiler knows the function exists.
- **Definition**: the same header **without** the semicolon, followed by the body
  in braces.
- **Call**: `factorial(5)` — the value 5 is the **argument**; inside the
  function `n` is the **parameter**.
- **return**: sends one value back and ends the function immediately. A `void`
  function returns nothing and may use a bare `return;` or none at all.

## 4.4 Accessing a function by passing values

When a function is called by passing values (**call by value**), the arguments
are *copied* into the parameters. The function works on the copies, so the
originals in the caller are untouched. This is C's default for everything except
arrays.

```c
float area(float l, float b) { return l * b; }
...
printf("area(8, 5)   = %.2f\n", area(8, 5));   /* prints 40.00 */
```

::: example Worked example 4.1 — a function that returns the larger of two numbers
**Problem.** Write a C program with a function `larger()` that takes two
integers and returns the greater, and call it from `main()`.

**Solution.**

```c
#include <stdio.h>
int larger(int a, int b);            /* prototype */

int main() {
    int x = 47, y = 92;
    printf("larger of %d and %d is %d\n", x, y, larger(x, y));
    return 0;
}

int larger(int a, int b) {           /* definition */
    if (a > b) return a;
    return b;
}
```

Compiled and run, this printed

```
larger of 47 and 92 is 92
```

The three marks go to the prototype, the `if` with two `return`s, and the call
used directly inside `printf`.
:::

## 4.5 Storage classes: automatic and external

A **storage class** decides four things about a variable: where it is stored,
its default initial value, its **scope** (where it can be seen) and its
**lifetime** (how long it survives).

```figure caption="Where each storage class lives in memory and how long it lasts. Automatic variables are created and destroyed with every call; external and static variables live for the whole run."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
fig, ax = plt.subplots(figsize=(4.9, 3.0))

blocks = [("CODE segment", "the compiled instructions", "#f3eefa", "#6a5acd", 0.42),
          ("DATA segment", "extern (global) and static variables\nlive for the whole program",
           "#eaf3ee", "#2e8b57", 0.62),
          ("HEAP", "malloc / calloc", "#f4f6f9", MUTED, 0.42),
          ("STACK", "auto (local) variables\ncreated on call, destroyed on return",
           "#eef4fa", ACCENT, 0.62)]
y = 0.25
for name, sub, fc, ec, h in blocks:
    ax.add_patch(Rectangle((0.20, y), 3.30, h, facecolor=fc, edgecolor=ec, lw=1.2))
    ax.text(0.34, y + h - 0.16, name, fontsize=7.0, color=INK, va="center")
    ax.text(0.34, y + (h - 0.34)/2 + 0.04, sub, fontsize=5.9, color=MUTED, va="center")
    y += h + 0.12

ax.annotate("", xy=(3.72, 2.62), xytext=(3.72, 2.10),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.0, mutation_scale=9))
ax.text(3.82, 2.36, "grows and shrinks\nwith every call",
        fontsize=5.9, color=ACCENT, va="center")
ax.text(3.82, 1.10, "one copy,\nkept until the\nprogram ends",
        fontsize=5.9, color="#2e8b57", va="center")
ax.text(0.20, 0.06, "register: asks for a CPU register (fast, no address)",
        fontsize=6.0, color=MUTED)
ax.set_xlim(0.0, 6.1); ax.set_ylim(0.0, 3.05)
ax.axis("off")
```

| Storage class | Keyword | Stored in | Default value | Scope | Lifetime |
|---|---|---|---|---|---|
| Automatic | `auto` (the default) | Stack | Garbage | Inside its own block | Until the block ends |
| External / global | `extern` | Data segment | 0 | The whole program, all files | Whole program |
| Static | `static` | Data segment | 0 | Its own block (or file) | Whole program |
| Register | `register` | CPU register if possible | Garbage | Inside its own block | Until the block ends |

```c
#include <stdio.h>

int counter_auto(void) {
    auto int c = 0;      /* created fresh on every call */
    c++;
    return c;
}
int counter_static(void) {
    static int c = 0;    /* keeps its value between calls */
    c++;
    return c;
}

extern int shared;       /* declared here, defined below */

void show(void) { printf("inside show(), shared = %d\n", shared); }

int shared = 100;        /* external (global) variable */

int main() {
    printf("auto  : %d %d %d\n", counter_auto(), counter_auto(), counter_auto());
    printf("static: %d %d %d\n", counter_static(), counter_static(), counter_static());
    shared = shared + 5;
    show();
    return 0;
}
```

Output:

```
auto  : 1 1 1
static: 1 2 3
inside show(), shared = 105
```

That output is the whole lesson: the automatic variable is born again on every
call and always returns 1, while the static variable survives between calls and
counts 1, 2, 3. The external variable `shared` is visible inside `show()`
without being passed to it.

::: caution An automatic variable starts with rubbish
`auto int c;` without `= 0` does **not** contain zero — it contains whatever
happened to be at that stack address. Only `extern` and `static` variables are
automatically initialised to 0. Forgetting this produces a program that gives a
different wrong answer every time it runs.
:::

## 4.6 Recursion: factorial and Fibonacci

::: definition Recursion
**Recursion** is a function calling itself, directly or indirectly. Every
recursive function needs a **base case** that stops the recursion and a
**recursive case** that moves towards it. Without a base case the calls never
stop and the program dies with a *stack overflow*.
:::

```figure caption="factorial(4) unwinding. The calls stack up until the base case is reached, then the values multiply back up the chain."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
fig, ax = plt.subplots(figsize=(4.9, 3.1))

calls = ["factorial(4) = 4 * factorial(3)",
         "factorial(3) = 3 * factorial(2)",
         "factorial(2) = 2 * factorial(1)",
         "factorial(1) = 1      base case"]
rets = ["= 24", "= 6", "= 2", "= 1"]
for i, (c, r) in enumerate(zip(calls, rets)):
    y = 2.45 - i*0.60
    fc = "#fdf3e6" if i == 3 else "#eef4fa"
    ec = "#c98a1e" if i == 3 else ACCENT
    ax.add_patch(FancyBboxPatch((0.30 + i*0.22, y), 2.95, 0.44,
                                boxstyle="round,pad=0.03", facecolor=fc,
                                edgecolor=ec, lw=1.1))
    ax.text(0.44 + i*0.22, y + 0.22, c, fontsize=6.2, color=INK, va="center",
            family="monospace")
    ax.text(3.45 + i*0.22, y + 0.22, r, fontsize=6.4, color="#2e8b57", va="center",
            family="monospace")
ax.annotate("", xy=(0.16, 2.87), xytext=(0.16, 0.74),
            arrowprops=dict(arrowstyle="-|>", color="#2e8b57", lw=1.2, mutation_scale=10))
ax.text(0.03, 1.80, "returning", fontsize=6.0, color="#2e8b57", rotation=90,
        va="center", ha="center")
ax.annotate("", xy=(4.62, 0.74), xytext=(4.62, 2.87),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2, mutation_scale=10))
ax.text(4.78, 1.80, "calls going down", fontsize=6.0, color=MUTED, rotation=270,
        va="center", ha="center")
ax.text(0.30, 0.30, "each call keeps its own copy of n on the stack",
        fontsize=6.2, color=MUTED)
ax.set_xlim(-0.05, 5.05); ax.set_ylim(0.12, 3.05)
ax.axis("off")
```

```c
#include <stdio.h>

long factorial(int n) {
    if (n == 0 || n == 1) return 1;      /* base case  */
    return n * factorial(n - 1);         /* recursive case */
}

int fibonacci(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    int i;
    printf("factorial: ");
    for (i = 0; i <= 8; i++) printf("%ld ", factorial(i));
    printf("\n5! = %ld,  7! = %ld\n", factorial(5), factorial(7));

    printf("Fibonacci series: ");
    for (i = 0; i < 10; i++) printf("%d ", fibonacci(i));
    printf("\n");
    return 0;
}
```

Output:

```
factorial: 1 1 2 6 24 120 720 5040 40320 
5! = 120,  7! = 5040
Fibonacci series: 0 1 1 2 3 5 8 13 21 34
```

| Point | Recursion | Iteration (loop) |
|---|---|---|
| Ends when | The base case is reached | The loop condition becomes false |
| Memory | A stack frame per call — heavy | One set of variables — light |
| Speed | Slower (call overhead) | Faster |
| Code length | Shorter and closer to the definition | Longer but plainer |
| Danger | Stack overflow if the base case is missing | Infinite loop |

## 4.7 Structure: definition, declaration, initialization and size

::: definition Structure
A **structure** is a user-defined data type that groups several variables —
possibly of **different types** — under one name. Each variable in it is called
a **member** or **field**.
:::

```c
struct student {              /* definition: a new type, no memory yet */
    int   roll;
    char  name[20];
    char  faculty[12];
    float marks;
};

struct student s1 = {1, "Anisha", "Science", 78.5};   /* declaration + init */
struct student s2;                                    /* declaration only   */
```

The definition creates a **template** and occupies no memory; memory is used
only when a variable of that type is declared. The size of a structure is the
sum of the sizes of its members, possibly rounded up by the compiler for
alignment — in the run below, `4 + 20 + 12 + 4 = 40` bytes.

## 4.8 Accessing members of a structure; array of structures

Members are reached with the **dot operator**, `s1.roll`. Strings cannot be
assigned with `=`; use `strcpy`. An **array of structures** holds many records of
the same kind — exactly what a class list, an inventory or a result sheet is.

```c
#include <stdio.h>
#include <string.h>

struct student {
    int   roll;
    char  name[20];
    char  faculty[12];
    float marks;
};

int main() {
    struct student s1 = {1, "Anisha", "Science", 78.5};
    struct student s2;
    struct student cls[3] = {
        {1, "Anisha",  "Science",    78.5},
        {2, "Bikash",  "Science",    52.0},
        {3, "Chandra", "Management", 85.0}
    };
    int i;
    float total = 0;

    s2.roll = 4;
    strcpy(s2.name, "Deepa");           /* strings need strcpy */
    strcpy(s2.faculty, "Science");
    s2.marks = 91.0;

    printf("%d %s %s %.1f\n", s1.roll, s1.name, s1.faculty, s1.marks);
    printf("%d %s %s %.1f\n", s2.roll, s2.name, s2.faculty, s2.marks);

    printf("--- array of structure ---\n");
    for (i = 0; i < 3; i++) {
        printf("%-3d %-8s %-11s %.1f\n",
               cls[i].roll, cls[i].name, cls[i].faculty, cls[i].marks);
        total += cls[i].marks;
    }
    printf("average = %.2f\n", total / 3);
    printf("sizeof(struct student) = %d bytes\n", (int)sizeof(struct student));
    return 0;
}
```

Output:

```
1 Anisha Science 78.5
4 Deepa Science 91.0
--- array of structure ---
1   Anisha   Science     78.5
2   Bikash   Science     52.0
3   Chandra  Management  85.0
average = 71.83
sizeof(struct student) = 40 bytes
```

## 4.9 Union: definition and declaration; union versus structure

::: definition Union
A **union** looks like a structure but all its members share **the same piece of
memory**. Its size is the size of its **largest** member, and only one member
holds a valid value at any moment.
:::

```figure caption="A structure gives every member its own memory; a union overlays them. Writing to one member of a union destroys the others."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(2, 1, figsize=(4.9, 2.9))

# structure
ax = axes[0]
segs = [("int i", 4, "#eef4fa"), ("float f", 4, "#eaf3ee"), ("char s[8]", 8, "#fdf3e6")]
x = 0.0
for name, w, fc in segs:
    ax.add_patch(Rectangle((x, 0.18), w*0.45, 0.50, facecolor=fc, edgecolor=INK, lw=1.0))
    ax.text(x + w*0.225, 0.43, name, ha="center", va="center", fontsize=6.4, color=INK)
    ax.text(x + w*0.225, 0.02, str(w) + " bytes", ha="center", fontsize=5.6, color=MUTED)
    x += w*0.45
ax.text(x + 0.18, 0.43, "total 16 bytes", fontsize=6.6, color=INK, va="center")
ax.set_title("struct: members side by side", fontsize=8.0, loc="left")
ax.set_xlim(-0.05, 10.0); ax.set_ylim(-0.08, 0.80); ax.axis("off")

# union
ax = axes[1]
ax.add_patch(Rectangle((0.0, 0.18), 8*0.45, 0.50, facecolor="#fdecec",
                       edgecolor="#d9534f", lw=1.3))
ax.text(8*0.225, 0.43, "the SAME 8 bytes", ha="center", va="center", fontsize=6.6,
        color=INK)
for x, name, col in [(0.62, "int i", ACCENT), (1.80, "float f", "#2e8b57"),
                     (2.98, "char s[8]", "#c98a1e")]:
    ax.text(x, 1.12, name, fontsize=6.2, color=col, ha="center")
    ax.annotate("", xy=(x, 0.72), xytext=(x, 1.02),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0, mutation_scale=8))
ax.text(8*0.45 + 0.18, 0.43, "total 8 bytes", fontsize=6.6, color=INK, va="center")
ax.text(8*0.45 + 0.18, 1.08, "all three names point at\nthe very same bytes",
        fontsize=5.8, color=MUTED, va="center")
ax.set_title("union: members overlaid", fontsize=8.0, loc="left")
ax.set_xlim(-0.05, 10.0); ax.set_ylim(0.05, 1.40); ax.axis("off")
fig.subplots_adjust(hspace=0.75)
```

```c
union value {
    int   i;
    float f;
    char  s[8];
};
...
union value v;
printf("sizeof(union value)    = %d bytes\n", (int)sizeof(union value));
v.i = 65;      printf("union after v.i = 65   : v.i = %d\n", v.i);
v.f = 3.14f;   printf("union after v.f = 3.14 : v.f = %.2f, v.i = %d (corrupted)\n",
                      v.f, v.i);
```

Output:

```
sizeof(union value)    = 8 bytes
union after v.i = 65   : v.i = 65
union after v.f = 3.14 : v.f = 3.14, v.i = 1078523331 (corrupted)
```

| Point | Structure | Union |
|---|---|---|
| Keyword | `struct` | `union` |
| Memory | Separate memory for every member | One shared memory for all members |
| Size | Sum of all members (here 40 bytes) | Size of the largest member (here 8 bytes) |
| Members usable at once | All | Only one |
| Changing one member | Does not affect the others | Overwrites all the others |
| Initialisation | All members may be initialised | Only the first member may be initialised |
| Use | Records with several fields at once | Saving memory when only one field is needed at a time |

::: caution The union output above proves it
After `v.f = 3.14`, reading `v.i` gave **1078523331** — the bit pattern of the
float read as an integer. A union does not convert; it reinterprets the same
bytes. Read back only the member you wrote last.
:::

## 4.10 Pointers: definition; the address (&) and indirection (*) operators

::: definition Pointer
A **pointer** is a variable that stores the **memory address** of another
variable. `int *p;` declares p as a pointer to an int; `p = &n;` makes it point
at `n`; `*p` is the value stored at that address.
:::

```figure caption="n holds a value; p holds n's address. *p and n are two names for the same box of memory."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(4.9, 2.4))

# variable n
ax.add_patch(Rectangle((0.55, 1.25), 1.30, 0.55, facecolor="#eef4fa",
                       edgecolor=ACCENT, lw=1.3))
ax.text(1.20, 1.52, "25", ha="center", va="center", fontsize=9.0, color=INK)
ax.text(1.20, 1.96, "int n", ha="center", fontsize=7.2, color=INK)
ax.text(1.20, 1.06, "address 0x7ffc...26bc", ha="center", fontsize=5.8, color=MUTED)

# pointer p
ax.add_patch(Rectangle((3.55, 1.25), 1.75, 0.55, facecolor="#eaf3ee",
                       edgecolor="#2e8b57", lw=1.3))
ax.text(4.42, 1.52, "0x7ffc...26bc", ha="center", va="center", fontsize=7.0, color=INK)
ax.text(4.42, 1.96, "int *p", ha="center", fontsize=7.2, color=INK)
ax.text(4.42, 1.06, "p holds an address", ha="center", fontsize=5.8, color=MUTED)

ax.annotate("", xy=(1.90, 1.52), xytext=(3.50, 1.52),
            arrowprops=dict(arrowstyle="-|>", color="#2e8b57", lw=1.3, mutation_scale=11,
                            connectionstyle="arc3,rad=0.22"))
ax.text(2.70, 2.02, "p = &n", ha="center", fontsize=6.8, color="#2e8b57",
        family="monospace")
ax.text(2.70, 0.86, "*p  is 25", ha="center", fontsize=6.8, color=ACCENT,
        family="monospace")
ax.text(0.30, 0.48, "&  address-of operator : gives the address of a variable",
        fontsize=6.4, color=MUTED)
ax.text(0.30, 0.24, "*  indirection operator : gives the value at an address",
        fontsize=6.4, color=MUTED)
ax.set_xlim(0.0, 6.0); ax.set_ylim(0.10, 2.25)
ax.axis("off")
```

<div style="break-before:page"></div>

## 4.11 Pointer expression and assignment; call by value and call by reference

```figure caption="Call by value copies the data, so the original cannot change. Call by reference copies the address, so the function reaches the original itself."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
fig, axes = plt.subplots(1, 2, figsize=(5.15, 2.7))

def cell(ax, x, y, t, fc, ec, w=0.68, h=0.42):
    ax.add_patch(Rectangle((x - w/2, y - h/2), w, h, facecolor=fc, edgecolor=ec, lw=1.1))
    ax.text(x, y, t, ha="center", va="center", fontsize=6.8, color=INK)

# ---- by value
ax = axes[0]
ax.text(1.5, 2.62, "main():  x = 10, y = 20", ha="center", fontsize=6.6, color=INK)
cell(ax, 1.05, 2.18, "10", "#eef4fa", ACCENT); cell(ax, 1.95, 2.18, "20", "#eef4fa", ACCENT)
ax.text(0.58, 2.18, "x", fontsize=6.4, color=MUTED, ha="center")
ax.text(2.42, 2.18, "y", fontsize=6.4, color=MUTED, ha="center")
ax.annotate("", xy=(1.05, 1.52), xytext=(1.05, 1.94),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, mutation_scale=8))
ax.annotate("", xy=(1.95, 1.52), xytext=(1.95, 1.94),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, mutation_scale=8))
ax.text(2.55, 1.74, "copy", fontsize=5.8, color=MUTED, ha="center")
ax.add_patch(FancyBboxPatch((0.35, 0.75), 2.30, 0.78, boxstyle="round,pad=0.04",
                            facecolor="#f4f6f9", edgecolor=MUTED, lw=1.0))
cell(ax, 1.05, 1.28, "10", "white", MUTED); cell(ax, 1.95, 1.28, "20", "white", MUTED)
ax.text(1.50, 0.92, "swap happens on the copies", ha="center", fontsize=5.8, color=MUTED)
ax.text(1.5, 0.42, "x = 10, y = 20\nUNCHANGED", ha="center", fontsize=6.6,
        color="#b02a37")
ax.set_title("call by value", fontsize=8.4)

# ---- by reference
ax = axes[1]
ax.text(1.5, 2.62, "main():  x = 10, y = 20", ha="center", fontsize=6.6, color=INK)
cell(ax, 1.05, 2.18, "10", "#eaf3ee", "#2e8b57"); cell(ax, 1.95, 2.18, "20", "#eaf3ee", "#2e8b57")
ax.text(0.58, 2.18, "x", fontsize=6.4, color=MUTED, ha="center")
ax.text(2.42, 2.18, "y", fontsize=6.4, color=MUTED, ha="center")
ax.add_patch(FancyBboxPatch((0.35, 0.75), 2.30, 0.78, boxstyle="round,pad=0.04",
                            facecolor="#f4f6f9", edgecolor=MUTED, lw=1.0))
cell(ax, 1.05, 1.28, "&x", "white", "#2e8b57"); cell(ax, 1.95, 1.28, "&y", "white", "#2e8b57")
ax.annotate("", xy=(1.05, 1.94), xytext=(1.05, 1.52),
            arrowprops=dict(arrowstyle="-|>", color="#2e8b57", lw=1.2, mutation_scale=9))
ax.annotate("", xy=(1.95, 1.94), xytext=(1.95, 1.52),
            arrowprops=dict(arrowstyle="-|>", color="#2e8b57", lw=1.2, mutation_scale=9))
ax.text(2.58, 1.74, "reaches\nthe original", fontsize=5.8, color="#2e8b57", ha="center")
ax.text(1.50, 0.92, "*a and *b change x and y", ha="center", fontsize=5.8, color=MUTED)
ax.text(1.5, 0.42, "x = 20, y = 10\nSWAPPED", ha="center", fontsize=6.6, color="#2e8b57")
ax.set_title("call by reference", fontsize=8.4)

for ax in axes:
    ax.set_xlim(0.0, 3.1); ax.set_ylim(0.12, 2.85); ax.axis("off")
fig.subplots_adjust(wspace=0.08)
```

```c
#include <stdio.h>

void swapByValue(int a, int b)      { int t = a; a = b; b = t; }
void swapByReference(int *a, int *b){ int t = *a; *a = *b; *b = t; }

int main() {
    int n = 25;
    int *p;             /* p is a pointer to int */
    p = &n;             /* & gives the address    */

    printf("n        = %d\n", n);
    printf("&n       = %p\n", (void *)&n);
    printf("p        = %p\n", (void *)p);
    printf("*p       = %d   (indirection: the value at that address)\n", *p);
    printf("sizeof(p)= %d bytes\n", (int)sizeof(p));

    *p = *p + 5;        /* pointer expression: changes n itself */
    printf("after *p = *p + 5,  n = %d\n", n);

    int x = 10, y = 20;
    swapByValue(x, y);
    printf("call by value    : x = %d, y = %d  (unchanged)\n", x, y);
    swapByReference(&x, &y);
    printf("call by reference: x = %d, y = %d  (swapped)\n", x, y);

    int arr[5] = {10, 20, 30, 40, 50};
    int *q = arr;                       /* an array name is the address of arr[0] */
    printf("arr[2] = %d,  *(q+2) = %d\n", arr[2], *(q + 2));
    return 0;
}
```

Output:

```
n        = 25
&n       = 0x7ffc003c26bc
p        = 0x7ffc003c26bc
*p       = 25   (indirection: the value at that address)
sizeof(p)= 8 bytes
after *p = *p + 5,  n = 30
call by value    : x = 10, y = 20  (unchanged)
call by reference: x = 20, y = 10  (swapped)
arr[2] = 30,  *(q+2) = 30
```

(The two addresses will differ on your machine; what matters is that `&n` and
`p` print the *same* address.)

| Point | Call by value | Call by reference |
|---|---|---|
| What is passed | A copy of the value | The address of the variable |
| Parameter declared as | `int a` | `int *a` |
| Call written as | `swap(x, y)` | `swap(&x, &y)` |
| Effect on the original | None | The original is changed |
| Memory | Extra copy of each argument | Only an address (8 bytes) |
| Returning several results | Not possible — `return` sends one value | Possible — change several variables through pointers |

## 4.12 Working with files: the concept of a data file; sequential and random files

A variable lives in RAM and dies when the program ends. A **data file** is a
named collection of bytes stored on disk, so the data survives, can be far
larger than memory, and can be shared between programs.

```figure caption="Sequential access must pass over every record to reach the tenth. Random access jumps straight to it with fseek."
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
fig, axes = plt.subplots(2, 1, figsize=(4.9, 2.6))

for k, (ax, title) in enumerate(zip(axes, ["Sequential file — records read in order",
                                           "Random-access file — jump to any record"])):
    for i in range(8):
        fc = "#fdf3e6" if i == 6 else "#eef4fa"
        ec = "#c98a1e" if i == 6 else ACCENT
        ax.add_patch(Rectangle((0.30 + i*0.56, 0.28), 0.50, 0.42,
                               facecolor=fc, edgecolor=ec, lw=1.0))
        ax.text(0.55 + i*0.56, 0.49, "R%d" % (i+1), ha="center", va="center",
                fontsize=5.8, color=INK)
    if k == 0:
        for i in range(6):
            ax.annotate("", xy=(0.84 + i*0.56, 0.86), xytext=(0.56 + i*0.56, 0.86),
                        arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=0.9,
                                        mutation_scale=7))
        ax.text(2.10, 1.08, "read R1 … R6 before reaching R7", fontsize=6.0,
                color=MUTED, ha="center")
    else:
        ax.annotate("", xy=(3.78, 0.74), xytext=(0.55, 0.74),
                    arrowprops=dict(arrowstyle="-|>", color="#2e8b57", lw=1.2,
                                    mutation_scale=9, connectionstyle="arc3,rad=-0.22"))
        ax.text(2.16, 1.32, "fseek(fp, 6*sizeof(rec), SEEK_SET)", fontsize=6.0,
                color="#2e8b57", ha="center", family="monospace")
    ax.set_title(title, fontsize=7.6, loc="left")
    ax.set_xlim(0.0, 5.0); ax.set_ylim(0.15, 1.50); ax.axis("off")
fig.subplots_adjust(hspace=0.85)
```

| Point | Sequential file | Random (direct) access file |
|---|---|---|
| Order of access | From the beginning, record by record | Any record directly |
| Speed for one record | Slow if it is far in | Fast — one jump |
| Functions | `fscanf`, `fprintf`, `getc`, `putc` | `fseek`, `ftell`, `rewind`, `fread`, `fwrite` |
| Record size | May vary | Usually fixed, so the position can be calculated |
| Typical use | Log files, text reports, payroll runs | Databases, indexed records, updating one record |

File **opening modes** used with `fopen(name, mode)`:

| Mode | Meaning | If the file does not exist | If it exists |
|---|---|---|---|
| `"r"` | Read only | Returns `NULL` | Opens it |
| `"w"` | Write only | Creates it | **Erases** the old contents |
| `"a"` | Append | Creates it | Adds at the end |
| `"r+"` | Read and write | Returns `NULL` | Opens it, keeps contents |
| `"w+"` | Read and write | Creates it | Erases the old contents |
| `"a+"` | Read and append | Creates it | Adds at the end |
| `"rb" "wb"` | The same in **binary** | | Used with `putw`, `getw`, `fread`, `fwrite` |

## 4.13 File manipulation functions: putw, getw, putc, getc, fscanf, fprintf

| Function | Purpose | Example |
|---|---|---|
| `fopen()` | Opens a file and returns a `FILE *` | `fp = fopen("a.txt", "w");` |
| `fclose()` | Closes it and flushes the buffer | `fclose(fp);` |
| `putc()` / `fputc()` | Writes one character | `putc('A', fp);` |
| `getc()` / `fgetc()` | Reads one character, returns `EOF` at the end | `ch = getc(fp);` |
| `putw()` | Writes one integer in binary | `putw(55, fp);` |
| `getw()` | Reads one integer in binary | `n = getw(fp);` |
| `fprintf()` | Formatted write — `printf` to a file | `fprintf(fp, "%d %s", r, nm);` |
| `fscanf()` | Formatted read — `scanf` from a file | `fscanf(fp, "%d %s", &r, nm);` |
| `fseek()` | Moves the file pointer | `fseek(fp, 8, SEEK_SET);` |
| `ftell()` | Reports the current position | `pos = ftell(fp);` |
| `rewind()` | Goes back to the beginning | `rewind(fp);` |

## 4.14 Opening, reading, writing and appending a data file

```figure caption="The life of every file program: declare a FILE pointer, open, check for NULL, work, close."
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon
fig, ax = plt.subplots(figsize=(4.6, 3.2))

def box(y, t, fc, ec, fs=6.8):
    ax.add_patch(FancyBboxPatch((0.55, y), 2.50, 0.42, boxstyle="round,pad=0.04",
                                facecolor=fc, edgecolor=ec, lw=1.1))
    ax.text(1.80, y + 0.21, t, ha="center", va="center", fontsize=fs, color=INK)

def down(y):
    ax.annotate("", xy=(1.80, y - 0.15), xytext=(1.80, y - 0.02),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, mutation_scale=8))

box(2.72, "FILE *fp;", "#f4f6f9", MUTED); down(2.72)
box(2.15, 'fp = fopen("student.txt", "w");', "#eef4fa", ACCENT, fs=6.2); down(2.15)
ax.add_patch(Polygon([(1.80, 1.92), (2.75, 1.60), (1.80, 1.28), (0.85, 1.60)],
                     facecolor="#fff3cd", edgecolor="#c98a1e", lw=1.0))
ax.text(1.80, 1.60, "fp == NULL ?", ha="center", va="center", fontsize=6.2, color=INK)
ax.annotate("", xy=(3.75, 1.60), xytext=(2.80, 1.60),
            arrowprops=dict(arrowstyle="-|>", color="#d9534f", lw=1.0, mutation_scale=8))
ax.text(3.80, 1.60, "print an error\nand exit", fontsize=6.0, color="#d9534f",
        va="center")
ax.text(3.20, 1.74, "yes", fontsize=5.6, color="#d9534f", ha="center")
ax.annotate("", xy=(1.80, 1.12), xytext=(1.80, 1.26),
            arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.0, mutation_scale=8))
ax.text(1.95, 1.19, "no", fontsize=5.6, color=MUTED)
box(0.70, "fprintf / fscanf / getc / putw", "#eaf3ee", "#2e8b57", fs=6.2); down(0.70)
box(0.13, "fclose(fp);", "#f3eefa", "#6a5acd")
ax.set_xlim(0.0, 6.0); ax.set_ylim(0.00, 3.30)
ax.axis("off")
```

The program below writes a text file, reads it back with `fscanf`, appends a
record, dumps the whole file with `getc`, then repeats the exercise in binary
with `putw`/`getw` and finally jumps straight to the third integer with `fseek`.

```c
#include <stdio.h>

int main() {
    FILE *fp;
    char ch;
    int  n, i;
    char name[20];
    float marks;

    /* ---- 1. WRITE a text file with fprintf ---- */
    fp = fopen("student.txt", "w");
    if (fp == NULL) { printf("Cannot open file\n"); return 1; }
    fprintf(fp, "%d %s %.1f\n", 1, "Anisha",  78.5);
    fprintf(fp, "%d %s %.1f\n", 2, "Bikash",  52.0);
    fprintf(fp, "%d %s %.1f\n", 3, "Chandra", 85.0);
    fclose(fp);
    printf("written student.txt\n");

    /* ---- 2. READ it back with fscanf ---- */
    fp = fopen("student.txt", "r");
    printf("--- reading with fscanf ---\n");
    while (fscanf(fp, "%d %s %f", &n, name, &marks) != EOF)
        printf("roll %d  %-8s %.1f\n", n, name, marks);
    fclose(fp);

    /* ---- 3. APPEND ---- */
    fp = fopen("student.txt", "a");
    fprintf(fp, "%d %s %.1f\n", 4, "Deepa", 91.0);
    fclose(fp);

    /* ---- 4. READ character by character with getc ---- */
    fp = fopen("student.txt", "r");
    printf("--- reading with getc after appending ---\n");
    while ((ch = getc(fp)) != EOF) putchar(ch);
    fclose(fp);

    /* ---- 5. putw and getw: integers in a binary file ---- */
    fp = fopen("marks.dat", "wb");
    for (i = 1; i <= 5; i++) putw(i * 11, fp);
    fclose(fp);
    fp = fopen("marks.dat", "rb");
    printf("--- integers read back with getw ---\n");
    for (i = 1; i <= 5; i++) printf("%d ", getw(fp));
    printf("\n");

    /* ---- 6. RANDOM access with fseek and ftell ---- */
    fseek(fp, 2 * sizeof(int), SEEK_SET);   /* jump straight to the 3rd integer */
    printf("3rd integer directly = %d, position now = %ld\n", getw(fp), ftell(fp));
    fclose(fp);
    return 0;
}
```

Output:

```
written student.txt
--- reading with fscanf ---
roll 1  Anisha   78.5
roll 2  Bikash   52.0
roll 3  Chandra  85.0
--- reading with getc after appending ---
1 Anisha 78.5
2 Bikash 52.0
3 Chandra 85.0
4 Deepa 91.0
--- integers read back with getw ---
11 22 33 44 55 
3rd integer directly = 33, position now = 12
```

::: example Worked example 4.2 — why `fseek` landed on 33
**Problem.** Explain the last line of the output: why does
`fseek(fp, 2 * sizeof(int), SEEK_SET)` reach the third integer, and why does
`ftell` then report 12?

**Solution.** `putw` wrote the five integers 11, 22, 33, 44, 55 in binary, each
occupying `sizeof(int) = 4` bytes, so the file is 20 bytes long:

| Byte offset | 0–3 | 4–7 | 8–11 | 12–15 | 16–19 |
|---|---|---|---|---|---|
| Value | 11 | 22 | 33 | 44 | 55 |

`SEEK_SET` measures from the start of the file, and $2 \times 4 = 8$, so the
file pointer is placed at byte 8 — the first byte of the third integer. `getw`
then reads 4 bytes (33) and leaves the pointer at $8 + 4 = 12$, which is what
`ftell` reports. This calculation, `offset = (record number) × (record size)`,
is the whole idea of random access.
:::

::: example Worked example 4.3 — write and read a structure to a file
**Problem.** Write a C program that stores three student records in a file and
reads them back.

**Solution.** Use `fprintf`/`fscanf` for a text file, as in section 4.14, or
`fwrite`/`fread` for a binary file:

```c
#include <stdio.h>
struct student { int roll; char name[20]; float marks; };

int main() {
    FILE *fp;
    struct student s[3] = {{1,"Anisha",78.5},{2,"Bikash",52.0},{3,"Chandra",85.0}};
    struct student t;
    int i;

    fp = fopen("stud.dat", "wb");
    if (fp == NULL) { printf("Cannot open file\n"); return 1; }
    fwrite(s, sizeof(struct student), 3, fp);      /* write all 3 at once */
    fclose(fp);

    fp = fopen("stud.dat", "rb");
    for (i = 0; i < 3; i++) {
        fread(&t, sizeof(struct student), 1, fp);
        printf("%d %-8s %.1f\n", t.roll, t.name, t.marks);
    }
    fclose(fp);
    return 0;
}
```

Compiled and run, this printed

```
1 Anisha   78.5
2 Bikash   52.0
3 Chandra  85.0
```

Marks are given for the `"wb"`/`"rb"` modes, the `NULL` check, `sizeof(struct
student)` as the record size, and closing the file after each phase.
:::

```photogrid label="4.P" cols="2" ratio="1.27" caption="C was written by Dennis Ritchie, and a structure in C shows how the compiler places data in memory. (a) Ritchie receiving the Japan Prize. (b) The ctypes module reports that a struct holding char, int, char and double occupies 24 bytes, though its fields need only 14. The compiler inserts padding so that the int starts at a multiple of 4 and the double at offset 16. Declaring the members in order of size, double then int then the two chars, gives 16 bytes. The record shrinks by 8 bytes, which matters when a program stores a million of them in an array or a binary file."
@ photo id="cs12/ritchie" cap="Dennis Ritchie (right), who created the C language at Bell Labs"
fit 1.27
focus 0.5 0.5
@ svg cap="Struct padding measured with ctypes"
import ctypes
class A(ctypes.Structure):
    _fields_ = [("a", ctypes.c_char), ("b", ctypes.c_int), ("c", ctypes.c_char), ("d", ctypes.c_double)]
class B(ctypes.Structure):
    _fields_ = [("d", ctypes.c_double), ("b", ctypes.c_int), ("a", ctypes.c_char), ("c", ctypes.c_char)]
sa, sb = ctypes.sizeof(A), ctypes.sizeof(B)
assert (sa, sb) == (24, 16) and A.b.offset == 4 and A.d.offset == 16
def strip(y, T, names, col):
    used = {}
    for n in names:
        fld = getattr(T, n)
        used[n] = (fld.offset, fld.size)
    w = 11
    for i in range(ctypes.sizeof(T)):
        f.box(8 + i * w, y, w - 1, 16, fill="#e2e8f0", stroke="#cbd5e1", sw=0.6, r=1)
    for n, (o, s) in used.items():
        f.box(8 + o * w, y, s * w - 1, 16, fill=col[n], stroke=NAVY, sw=1, r=1)
        f.text(8 + o * w + s * w / 2, y + 8, n, size=9, color=NAVY, bold=True, vmid=True)
col = dict(a=SAND, b=BLUE, c=ROSE, d=MINT)
f = Fig(300, 236)
f.text(150, 14, "Bytes of a struct: grey cells are padding", size=10.5, color=NAVY, bold=True)
f.text(8, 40, "char a; int b; char c; double d;", size=10, color=SLATE, bold=True, anchor="start")
strip(48, A, "abcd", col)
f.text(8, 40 + 70, "double d; int b; char a; char c;", size=10, color=SLATE, bold=True, anchor="start")
strip(118, B, "dbac", col)
f.text(150, 176, "top: sizeof = %d bytes" % sa, size=10.5, color=RED, bold=True)
f.text(150, 208, "bottom: sizeof = %d bytes" % sb, size=10.5, color=TEAL, bold=True)
f.text(150, 224, "8 bytes saved per record", size=10, color=SLATE, bold=True)
facts = dict(sa=sa, sb=sb, save=sa - sb, off=A.d.offset)
```

## Chapter summary

- A C program is a set of functions; `main()` is the one that runs first.
  A function needs a **prototype**, a **definition** and a **call**, and
  `return` sends back exactly one value.
- Library functions come from headers (`stdio.h`, `math.h`, `string.h`);
  user-defined functions are written by the programmer. Functions give
  reusability, modularity, readability and easier debugging.
- Storage classes: `auto` (stack, garbage, block scope, dies with the block),
  `extern` (data segment, 0, whole program), `static` (data segment, 0, block
  scope but whole-program lifetime), `register` (in a CPU register).
- **Recursion** needs a base case. `factorial(5) = 120`; the Fibonacci series is
  0 1 1 2 3 5 8 13 21 34. Recursion is shorter but uses a stack frame per call.
- A **structure** groups members of different types, each with its own memory;
  its size is the sum of the members. A **union** overlays its members in one
  block the size of the largest, so only the member written last is valid.
  Members are reached with `.`; an **array of structures** stores many records.
- A **pointer** stores an address. `&` gives the address, `*` gives the value at
  an address. **Call by value** passes copies and cannot change the original;
  **call by reference** passes addresses and can.
- A **data file** stores data permanently. **Sequential** access reads records in
  order; **random** access jumps with `fseek`. The pattern is always
  `FILE *fp;` → `fopen` → check `NULL` → `fprintf`/`fscanf`/`getc`/`putw` →
  `fclose`. Mode `"w"` erases an existing file; use `"a"` to append.

## Practice questions

**Group A — Multiple choice (1 mark each)**

1. Which storage class keeps its value between function calls? <span class="marks">[1]</span>
   (a) auto (b) register (c) static (d) none
2. What does `&` mean when written before a variable name? <span class="marks">[1]</span>
   (a) the value of (b) the address of (c) logical AND (d) a pointer declaration
3. The size of a union is the size of <span class="marks">[1]</span>
   (a) all members added (b) its largest member (c) its first member (d) 8 bytes always
4. Which file mode erases the contents of an existing file? <span class="marks">[1]</span>
   (a) `"r"` (b) `"a"` (c) `"w"` (d) `"r+"`
5. A recursive function without a base case will <span class="marks">[1]</span>
   (a) return 0 (b) not compile (c) overflow the stack (d) run once
6. `getw()` reads <span class="marks">[1]</span>
   (a) one character (b) one word of text (c) one integer (d) one line
7. In call by value, changes made to the parameters inside a function <span class="marks">[1]</span>
   (a) change the arguments (b) do not change the arguments (c) cause an error (d) change only globals

::: note Answers to Group A
**1.** (c) — `static` has block scope but whole-program lifetime.
**2.** (b) — `&` is the address-of operator; `*` is indirection.
**3.** (b) — all members share the same memory.
**4.** (c) — `"w"` truncates; use `"a"` to keep the old data.
**5.** (c) — the calls never stop and the stack runs out.
**6.** (c) — `getw`/`putw` work on integers in binary files.
**7.** (b) — the function works on copies.
:::

**Group B — Short answer (5 marks each)**

1. What is a function? Differentiate between library and user-defined functions
   and list any four advantages of using functions. <span class="marks">[5]</span>
2. Explain the automatic and external storage classes with their scope, default
   value and lifetime, and illustrate the difference with a short program. <span class="marks">[5]</span>
3. What is recursion? Write a C program to find the factorial of a number using
   recursion and dry-run it for $n = 4$. <span class="marks">[5]</span>
4. Differentiate between a structure and a union on any five points, with a
   declaration of each. <span class="marks">[5]</span>
5. Define a pointer. Explain the `&` and `*` operators and write a program that
   swaps two numbers using call by reference. <span class="marks">[5]</span>
6. What is a data file? Differentiate between sequential and random access
   files, and name the file modes `"r"`, `"w"` and `"a"`. <span class="marks">[5]</span>

::: note Answer to Group B question 3 — dry run for n = 4
`factorial(4)` calls `factorial(3)`, which calls `factorial(2)`, which calls
`factorial(1)`. `factorial(1)` hits the base case and returns 1. Then
$2 \times 1 = 2$ is returned, then $3 \times 2 = 6$, then $4 \times 6 = 24$. So
`factorial(4)` is **24**, which matches the printed series
`1 1 2 6 24 120 720 5040 40320` in section 4.6.
:::

::: note Answers to Group B questions 1, 2, 4, 5 and 6
**1.** A **function** is a named, self-contained block of statements that performs
one task and may be called from many places; it takes arguments and may return a
value. A **library function** is already written and stored in a standard header,
for example `printf()` (`stdio.h`), `sqrt()` (`math.h`) and `strlen()`
(`string.h`); the programmer only includes the header and calls it. A
**user-defined function** is written by the programmer for a particular job, for
example `int factorial(int n)`. Library functions are tested, fast to use and cannot
be changed, whereas user-defined functions fit the problem exactly but must be
written, tested and maintained by the programmer. Four advantages of functions:
**(i)** a program is divided into small, easy-to-understand parts (modularity);
**(ii)** code written once is reused many times, so the program is shorter;
**(iii)** errors are easy to find because each function can be tested separately;
**(iv)** many programmers can work on different functions of a large project. Other
advantages are easier maintenance and the ability to build libraries.

**2.**

| Point | Automatic (`auto`) | External (`extern`) |
|---|---|---|
| Declared | Inside a function or block | Outside all functions (global) |
| Scope | Only that function or block | Whole program, in every function |
| Default value | Garbage (undefined) | Zero |
| Lifetime | Created on entry, destroyed on exit | Whole run of the program |
| Memory | Stack | Data segment |

```c
int g = 5;                       /* external: visible everywhere */
void demo(void) {
    int a = 1;                   /* automatic: new copy on every call */
    a++;
    g++;
    printf("a=%d g=%d\n", a, g);
}
```
Calling `demo()` twice prints `a=2 g=6` and then `a=2 g=7`. The automatic variable
`a` starts again at 1 on every call, so it is always 2 after the increment, while the
external variable `g` remembers its value between calls and keeps growing.

**4.**

| Point | Structure | Union |
|---|---|---|
| Keyword | `struct` | `union` |
| Memory | Separate space for every member | One space shared by all members |
| Size | Sum of member sizes (plus padding) | Size of the largest member |
| Access | All members usable at once | Only one member holds a valid value at a time |
| Use | A record such as a student | Saving memory when one of several values is needed |

```c
struct Student { int roll; char name[20]; float marks; };   /* sizeof = 28 bytes */
union  Data    { int i; float f; char s[20]; };              /* sizeof = 20 bytes */
```
On a typical machine the structure takes 4 + 20 + 4 = 28 bytes, while the union
takes only 20 bytes, the size of its largest member `s`. Writing to one member of a
union overwrites the others.

**5.** A **pointer** is a variable that stores the *address* of another variable.
It is declared with `*`, for example `int *p;`. The **address-of operator `&`**
gives the address of a variable: `p = &x;` stores the address of `x` in `p`. The
**indirection (dereference) operator `*`** gives the value stored at the address:
`*p` is the value of `x`. In **call by reference** the addresses are passed, so the
function changes the original variables.

```c
void swap(int *a, int *b) { int t = *a; *a = *b; *b = t; }
int main(void) {
    int x = 10, y = 20;
    swap(&x, &y);
    printf("x=%d y=%d\n", x, y);   /* prints x=20 y=10 */
    return 0;
}
```
Because `swap` works on the addresses of `x` and `y`, the values are really
exchanged in `main`. With call by value, only copies would be swapped and `x` and `y`
would stay 10 and 20.

**6.** A **data file** is a named collection of data stored permanently on a disk, so
that it remains after the program ends. In a **sequential file** the records are read
or written one after another from the start, and to reach the 100th record the first
99 must be passed; text files made with `fprintf` are of this kind. In a **random
(direct) access file** the program can jump straight to any record with `fseek()`
without reading the earlier ones, which is faster for large files such as a database.
File modes: `"r"` opens an existing file for **reading** (it fails if the file does
not exist); `"w"` opens a file for **writing** and creates it, or erases the old
contents if it exists; `"a"` opens a file for **appending**, so new data are added at
the end and the old data are kept. Always check that `fopen()` did not return `NULL`
and always close the file with `fclose()`.
:::

**Group C — Long answer (8 marks each)**

1. (a) What is a structure? Write a C program that reads the roll number, name
   and marks of 3 students into an **array of structures** and prints them along
   with the average marks. <span class="marks">[5]</span>
   (b) Differentiate between a structure and a union with an example showing the
   size of each. <span class="marks">[3]</span>

2. (a) Explain call by value and call by reference with a program that attempts
   to swap two numbers by each method, and state what is printed in each case. <span class="marks">[5]</span>
   (b) Write a C program to create a data file `student.txt`, write three records
   into it and read them back. <span class="marks">[3]</span>

::: note Answer outline to Group C question 2
Part (a): the program in section 4.11 is the complete answer. `swapByValue(x, y)`
prints `x = 10, y = 20` because it swapped its own copies; `swapByReference(&x,
&y)` prints `x = 20, y = 10` because `*a` and `*b` are the originals themselves.
Marks are for the two function definitions, the `&` in the second call, the
`int *` parameters, and stating both outputs.
Part (b): `fp = fopen("student.txt","w")`, a `NULL` check, three `fprintf`s,
`fclose`, then reopen with `"r"` and loop
`while (fscanf(fp, "%d %s %f", &n, name, &marks) != EOF)` — printed in full in
section 4.14.
:::


**Group D — Long answer (10 marks each), with full model answers**

1. What is a function? Explain the types, the parts of a function and the advantages with a program. <span class="marks">[10]</span>
2. What is a structure? Write a program with an array of structures and differentiate a structure from a union. <span class="marks">[10]</span>
3. Explain pointers, call by value and call by reference with programs. <span class="marks">[10]</span>

### Model answer D1: functions in C (10 marks)

**Introduction.** A **function** is a named block of statements that performs one task
and can be called whenever needed. Every C program has at least one function,
`main()`.

**Types.** **Library functions** are supplied with the compiler (`printf`, `sqrt`,
`strlen`). **User-defined functions** are written by the programmer.

**Parts of a function.**

1. **Function prototype (declaration):** tells the compiler the name, return type and
   parameters, e.g. `int factorial(int n);`
2. **Function definition:** the header and the body that contain the code.
3. **Function call:** a statement that uses the function, e.g. `f = factorial(5);`
4. **Return statement:** sends a value back and ends the function.

```c
#include <stdio.h>
int factorial(int n);                  /* prototype */
int main(void) {
    printf("%d\n", factorial(5));      /* call: prints 120 */
    return 0;
}
int factorial(int n) {                 /* definition */
    int f = 1, i;
    for (i = 2; i <= n; i++) f *= i;
    return f;                          /* return */
}
```

**Advantages.** (1) Modularity; (2) reuse of code; (3) shorter programs; (4) easy
testing and debugging; (5) teamwork on large programs; (6) easier maintenance; (7) a
function can be placed in a library; (8) it hides details from the caller.

| Basis | Library function | User-defined function |
|---|---|---|
| Written by | Compiler maker | Programmer |
| Header file | Needed (`stdio.h`) | Not needed |
| Can be changed | No | Yes |

**Conclusion.** Functions divide a large problem into small, testable pieces, which is
the basis of structured programming.

### Model answer D2: structure and union (10 marks)

**Introduction.** A **structure** is a user-defined data type that groups variables of
different types under one name; it models a record such as a student.

```c
#include <stdio.h>
struct Student { int roll; char name[20]; float marks; };
int main(void) {
    struct Student s[3] = {{1,"Anisha",78.5f},{2,"Bikash",64.0f},{3,"Chandra",91.5f}};
    float total = 0; int i;
    for (i = 0; i < 3; i++) {
        printf("%d %-8s %.1f\n", s[i].roll, s[i].name, s[i].marks);
        total += s[i].marks;
    }
    printf("Average = %.2f\n", total / 3);
    return 0;
}
```
This program prints the three records and `Average = 78.00` (78.5 + 64.0 + 91.5 =
234.0, and 234.0 / 3 = 78.0). Members are reached with the dot operator, and an array of
structures stores many records.

| Point | Structure | Union |
|---|---|---|
| Keyword | `struct` | `union` |
| Memory | Each member has its own space | All members share one space |
| Size of the example above | 28 bytes | 20 bytes (largest member) |
| Members in use | All together | One at a time |
| Use | Records | Saving memory |

**Conclusion.** A structure keeps related data together, an array of structures makes a
small database in memory, and a union saves memory when only one value is needed at a
time.

### Model answer D3: pointers and call by value / reference (10 marks)

**Introduction.** A **pointer** is a variable that holds the address of another
variable. `int *p = &x;` makes `p` point to `x`; `*p` reads or changes the value of
`x`.

**Operators.** `&` (address-of) gives the address of a variable. `*` (indirection)
gives the value at an address.

**Call by value.** The function receives copies of the arguments, so changes inside the
function do not affect the original variables.

```c
void swapByValue(int a, int b) { int t = a; a = b; b = t; }      /* swaps copies */
```
After `swapByValue(x, y)` with `x = 10` and `y = 20`, the output is still `x = 10, y = 20`.

**Call by reference.** The function receives addresses and works on the originals.

```c
void swapByReference(int *a, int *b) { int t = *a; *a = *b; *b = t; }
/* call: swapByReference(&x, &y); output: x = 20, y = 10 */
```

| Point | Call by value | Call by reference |
|---|---|---|
| What is passed | A copy of the value | The address |
| Effect on the original | None | Changes it |
| Parameters | `int a` | `int *a` |
| Use | Safe calculation | Swapping, returning many values |

**Advantages of pointers.** They allow dynamic memory, efficient passing of arrays and
structures, and several return values from a function.

**Conclusion.** Pointers give C its power over memory and are the key to call by
reference, but they must be used carefully because a wrong address can crash a
program.
