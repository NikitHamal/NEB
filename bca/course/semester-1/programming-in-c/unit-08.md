---
subject: Programming in C
grade: BCA Semester 1
unit: 8
title: The Preprocessor, the Build Process, Bit Operations and Linked Structures
hours: 8
area: BCA 102 · Programming in C · Units 4, 5, 7, 8 and 10 (extended topics and laboratory guide)
---

Units 1 to 7 teach the core of C. The TU outline names several topics that deserve more than a paragraph: the **C preprocessor** and the **build process** (unit 8 of the outline), the **bitwise and comma operators**, the **odd loop** and the **exit statement**, **parameterising `main`** with command-line arguments, **self-referential structures** with `typedef` and table lookup, and function **pointers**. This unit covers them with programs that were compiled and run, and ends with the laboratory work list for the whole course.

::: key What this unit gives you
- Macros (with and without arguments), `#` and `##`, macros versus functions, file inclusion, conditional compilation, `#undef`, `#pragma`.
- The five stages from source to running program: preprocessing, compiling, assembling, linking, loading.
- Bitwise operators, masks, shifts, bit-fields and the comma operator.
- The odd loop, `exit`, `break` with a flag, and `main(int argc, char *argv[])`.
- Self-referential structures, a linked list, `typedef`, table lookup, function pointers and callbacks.
- A laboratory checklist that maps every outline unit to practical programs.
:::

## 8.1 The C preprocessor in depth

The **preprocessor** is a text-processing step that runs *before* the compiler sees your code. It knows nothing about C types or syntax; it only replaces text. Every line that starts with `#` is a preprocessor **directive**.

| Directive | Purpose |
|---|---|
| `#include` | paste another file here |
| `#define`, `#undef` | create or remove a macro |
| `#if`, `#elif`, `#else`, `#endif` | include code only when a constant expression is true |
| `#ifdef`, `#ifndef` | include code only when a macro is (not) defined |
| `#pragma` | compiler-specific instruction |
| `#error`, `#line` | force an error message, change reported line numbers |

### Object-like macros

```c
#define PI 3.14159
#define MAX_STUDENTS 60
#define NEWLINE printf("\n")
```

Every later `PI` is replaced by `3.14159` before compilation. Unlike a `const` variable, a macro uses no memory and has no type, so it is also usable in places that need a constant expression, such as an array size.

### Function-like macros (macros with arguments)

```c
#include <stdio.h>
#define SQUARE(x) ((x) * (x))
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define BAD_SQUARE(x) x * x

int main(void)
{
    printf("SQUARE(2+3)     = %d\n", SQUARE(2 + 3));
    printf("BAD_SQUARE(2+3) = %d\n", BAD_SQUARE(2 + 3));
    printf("MAX(3, 9)       = %d\n", MAX(3, 9));
    return 0;
}
```
```output
SQUARE(2+3)     = 25
BAD_SQUARE(2+3) = 11
MAX(3, 9)       = 9
```

Two lessons are in this program. First, the **parentheses** matter: `BAD_SQUARE(2+3)` becomes `2+3 * 2+3 = 11` (see the output). Second, because a macro pastes its argument text, `SQUARE(i++)` (not run here) would become `((i++) * (i++))` and modify `i` **twice** in one expression; its result is undefined behaviour in C. Never pass an expression with side effects to a macro.

### The `#` and `##` operators

Inside a macro body `#x` turns the argument into a string literal (stringizing), and `a ## b` glues two tokens into one (token pasting).

```c
#include <stdio.h>
#define SHOW(expr) printf(#expr " = %d\n", (expr))
#define VAR(n) value##n

int main(void)
{
    int value1 = 10, value2 = 20;
    SHOW(value1 + value2);
    SHOW(VAR(2) * 3);
    return 0;
}
```
```output
value1 + value2 = 30
VAR(2) * 3 = 60
```

### Macros versus functions

| Point | Macro | Function |
|---|---|---|
| Processed by | preprocessor (text replacement) | compiler (a real call) |
| Type checking | none | arguments checked and converted |
| Speed | no call overhead, but code is repeated at every use | small call overhead, one copy of the code |
| Code size | grows with each use | stays small |
| Side effects | argument may be evaluated more than once | argument evaluated exactly once |
| Debugging | hard (the debugger sees expanded text) | easy |
| Recursion | impossible | possible |

Use a macro for named constants and tiny expressions; use a function (or `static inline`) for everything else.

### File inclusion

`#include <stdio.h>` searches the compiler's system directories; `#include "myutil.h"` searches the current directory first and then the system ones. A header should hold declarations (prototypes, `typedef`, macros), not definitions of variables or functions. Protect every header with an **include guard**, so including it twice does no harm:

```c
/* mathutil.h */
#ifndef MATHUTIL_H
#define MATHUTIL_H
int gcd(int a, int b);
#define ABS(x) ((x) < 0 ? -(x) : (x))
#endif
```

### Conditional compilation

```c
#include <stdio.h>
#define VERSION 2
#define DEBUG

int main(void)
{
#ifdef DEBUG
    printf("[debug] starting\n");
#endif
#if VERSION == 1
    printf("running version one\n");
#elif VERSION == 2
    printf("running version two\n");
#else
    printf("unknown version\n");
#endif
#undef DEBUG
#ifndef DEBUG
    printf("DEBUG is now undefined\n");
#endif
    printf("compiled from %s, line %d\n", "unit-08", __LINE__);
    return 0;
}
```
```output
[debug] starting
running version two
DEBUG is now undefined
compiled from unit-08, line 21
```

`#if` needs a constant integer expression (macros are replaced by their values; an undefined name counts as 0, and `defined(NAME)` tests for existence). `#undef NAME` removes a definition. Conditional compilation lets one source file serve several platforms, switch debugging output on and off, and keep a header from being included twice. The standard predefined macros `__FILE__`, `__LINE__`, `__DATE__`, `__TIME__` and `__func__` help in log messages.

### `#pragma`

`#pragma` gives the compiler an instruction that is not part of the language and may be ignored by other compilers. Common examples: `#pragma once` (a non-standard include guard accepted by GCC, Clang and MSVC), `#pragma pack(1)` (remove structure padding, which removes the 2 padding bytes from the `struct student` of unit 7 but makes access slower), and `#pragma warning(disable: ...)` on MSVC. Use `gcc -E file.c` to see exactly what the preprocessor produced.

## 8.2 The build process: from source to running program

A C program passes through five stages before its first line runs. Knowing them explains most error messages.

```svgfig label="8.1" caption="The build process. gcc -E stops after preprocessing, -S after compiling, -c after assembling; without a flag the linker produces the executable and the operating system loader runs it."
f = Fig(780, 230)
st = [("hello.c", "source text", "#ffffff"), ("hello.i", "preprocessed", BLUE), ("hello.s", "assembly", SOFT), ("hello.o", "object code", BLUE), ("a.out", "executable", SOFT)]
x = 12
for i, (n, d, c) in enumerate(st):
    f.box(x, 40, 120, 52, n, fill=c, stroke=NAVY, size=11, bold=True)
    f.text(x + 60, 112, d, size=10, color=SLATE)
    if i < 4:
        f.arrow([(x + 120, 66), (x + 148, 66)], color=NAVY)
    x += 150
for i, (n, flag) in enumerate([("1 Preprocess", "gcc -E"), ("2 Compile", "gcc -S"), ("3 Assemble", "gcc -c"), ("4 Link", "libc + other .o")]):
    f.text(12 + 135 + i * 150, 30, n, size=10, color=TEAL, bold=True)
    f.text(12 + 135 + i * 150, 150, flag, size=10, color=SLATE)
f.box(150, 176, 480, 38, "5 Load: the operating system copies a.out into memory and starts main", fill="#fef3c7", stroke=NAVY, size=10.5, bold=True)
```

1. **Preprocessing** expands `#include` and macros, removes comments and drops the code that conditional compilation excludes.
2. **Compiling** checks syntax and types and translates C into assembly language for the target processor. Syntax errors appear here.
3. **Assembling** converts assembly into machine code, producing an **object file** (`.o` or `.obj`) that still has unresolved references.
4. **Linking** joins your object files with library code (`printf` lives in the C library) and resolves every reference. An *undefined reference to `foo`* error comes from this stage: you declared and called `foo` but never defined it.
5. **Loading** is done by the operating system: it allocates memory, copies the code and data in, and starts `main`.

```text
gcc -E hello.c -o hello.i     # stage 1 only
gcc -S hello.i                # stages 1-2, produces hello.s
gcc -c hello.s                # stages 1-3, produces hello.o
gcc hello.o -o hello          # link
./hello                       # load and run
```

With several files, `gcc main.c util.c -o app` compiles each file separately and links them once. Changing only `util.c` means only `util.o` needs recompiling, which is the idea behind the `make` tool.

## 8.3 Bitwise operators, masks and bit-fields

Bitwise operators work on the individual bits of integers. They are the tools of device drivers, flags, network headers and compact data.

| Operator | Name | Example (`a = 12` = 1100, `b = 10` = 1010) | Result |
|---|---|---|---|
| `&` | AND | `a & b` | 1000 = 8 |
| `\|` | OR | `a \| b` | 1110 = 14 |
| `^` | XOR | `a ^ b` | 0110 = 6 |
| `~` | complement | `~a` | all bits flipped |
| `<<` | left shift | `a << 2` | 110000 = 48 (multiply by 2²) |
| `>>` | right shift | `a >> 2` | 11 = 3 (divide by 2²) |

The four masking idioms for bit number `n` (0 = least significant) are: **set** `x |= (1u << n)`, **clear** `x &= ~(1u << n)`, **toggle** `x ^= (1u << n)` and **test** `(x >> n) & 1`.

```c
#include <stdio.h>

#define READ  (1u << 0)
#define WRITE (1u << 1)
#define EXEC  (1u << 2)

void show(const char *label, unsigned x)
{
    printf("%-8s", label);
    for (int i = 7; i >= 0; i--)
        putchar(((x >> i) & 1u) ? '1' : '0');
    printf("  (%u)\n", x);
}

int main(void)
{
    unsigned a = 12, b = 10, perm = 0;
    show("a", a);
    show("b", b);
    show("a & b", a & b);
    show("a | b", a | b);
    show("a ^ b", a ^ b);
    show("a << 2", a << 2);
    show("a >> 2", a >> 2);
    perm |= READ | WRITE;
    show("perm", perm);
    perm &= ~WRITE;
    perm ^= EXEC;
    show("perm", perm);
    printf("can read? %s\n", (perm & READ) ? "yes" : "no");
    printf("is 40 a power of two? %s\n", (40 & 39) == 0 ? "yes" : "no");
    printf("is 64 a power of two? %s\n", (64 & 63) == 0 ? "yes" : "no");
    return 0;
}
```
```output
a       00001100  (12)
b       00001010  (10)
a & b   00001000  (8)
a | b   00001110  (14)
a ^ b   00000110  (6)
a << 2  00110000  (48)
a >> 2  00000011  (3)
perm    00000011  (3)
perm    00000101  (5)
can read? yes
is 40 a power of two? no
is 64 a power of two? yes
```

`x & (x - 1)` clears the lowest set bit, so it is zero exactly when `x` has one bit set (a power of two). Shifting a negative signed value right is implementation-defined and shifting by the width of the type or more is undefined: use `unsigned` for bit work.

### Bit-fields

A **bit-field** packs small members into a few bits of a structure:

```c
#include <stdio.h>

struct date {
    unsigned day   : 5;   /* 1..31 */
    unsigned month : 4;   /* 1..12 */
    unsigned year  : 7;   /* years since 2000, 0..127 */
};

int main(void)
{
    struct date d = {14, 4, 82};
    printf("date = %u/%u/%u\n", d.day, d.month, 2000u + d.year);
    printf("sizeof(struct date) = %zu bytes\n", sizeof d);
    return 0;
}
```
```output
date = 14/4/2082
sizeof(struct date) = 4 bytes
```

The 16 bits fit in a 4-byte `unsigned` unit, so the structure is 4 bytes, not 12. You cannot take the address of a bit-field, and the layout (bit order) is compiler-dependent, so do not use bit-fields to match an external file or network format.

### The comma and `sizeof` operators

The **comma operator** evaluates its left operand, discards it, and gives the value of the right operand; it has the lowest precedence of all operators. Its main use is in a `for` header, `for (i = 0, j = n - 1; i < j; i++, j--)`. Beware: `int x = (3, 5);` gives 5, whereas `int a = 3, b = 5;` is a declaration with a different comma. `sizeof` is a compile-time operator that gives the size in bytes of a type or expression, as a `size_t`; `sizeof(arr) / sizeof(arr[0])` gives the number of elements of a true array (but not of a pointer parameter).

## 8.4 The odd loop, `exit`, and parameterising `main`

### The odd loop

A loop whose natural exit comes in the **middle** of the body (after reading a value but before processing it) is called an *odd loop*. The clean C form is an infinite loop with an explicit `break`:

```c
#include <stdio.h>

int main(void)
{
    int n, sum = 0, count = 0;
    for (;;) {                       /* odd loop: exit in the middle */
        printf("enter a mark (-1 to stop): ");
        if (scanf("%d", &n) != 1 || n < 0)
            break;
        sum += n;
        count++;
    }
    if (count > 0)
        printf("\n%d marks, average %.2f\n", count, (double)sum / count);
    else
        printf("\nno marks entered\n");
    return 0;
}
```
```input
70 85 90 -1
```
```output
enter a mark (-1 to stop): enter a mark (-1 to stop): enter a mark (-1 to stop): enter a mark (-1 to stop): 
3 marks, average 81.67
```

Compare it with the usual pattern that repeats the input statement before the loop and again at its end; the odd loop writes the `scanf` once. **Controlling the loop execution**: `break` leaves the nearest loop, `continue` skips to the next iteration (to the update expression in a `for`), `goto` jumps to a label (use it only to escape deeply nested loops), and `return` leaves the whole function.

### The `exit` statement

`exit(status)` from `<stdlib.h>` ends the **whole program** at once from any function, flushing and closing open files. `exit(0)` or `exit(EXIT_SUCCESS)` signals success, `exit(EXIT_FAILURE)` signals failure. `return` in `main` is equivalent to `exit`, but `return` in another function only leaves that function. `abort()` ends the program abnormally without cleanup.

### Command-line arguments

The full prototype of `main` lets the operating system pass the words typed after the program name:

```c
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    printf("argument count (argc) = %d\n", argc);
    for (int i = 1; i < argc; i++)
        printf("argv[%d] = \"%s\"\n", i, argv[i]);
    if (argc < 3) {
        printf("usage: add number number\n");
        return EXIT_FAILURE;
    }
    int a = atoi(argv[1]), b = atoi(argv[2]);
    printf("%d + %d = %d\n", a, b, a + b);
    return EXIT_SUCCESS;
}
```
```output
argument count (argc) = 1
usage: add number number
```

Run without arguments (this is the output that the test harness captures), the program prints its usage line and exits with a failure status. Run as `./add 12 30` it prints:

```text
argument count (argc) = 3
argv[1] = "12"
argv[2] = "30"
12 + 30 = 42
```

`argc` is the number of words including the program name, and `argv` is an array of `argc + 1` strings whose last element is `NULL`. Running `./add 12 30` gives `argc = 3`, `argv[0] = "./add"`, `argv[1] = "12"`, `argv[2] = "30"`; the arguments are always **strings**, so convert them with `atoi`, `atof` or the safer `strtol`. Many tools you use daily (`gcc`, `ls`, `cp`) are exactly this: `cp a.txt b.txt` is `argc = 3`.

## 8.5 Self-referential structures, `typedef` and table lookup

A structure cannot contain itself, but it **can contain a pointer to its own type**. Such a *self-referential* structure is the building block of linked lists, trees and graphs.

```c
struct node {
    int data;
    struct node *next;       /* pointer to another node of the same type */
};
```

`typedef` gives a type a new name, which shortens declarations: `typedef struct node Node;` (or `typedef struct node { ... } Node;`). A `typedef` creates no new type and, unlike a macro, is understood by the compiler, so `typedef int *IntPtr;` makes `IntPtr a, b;` two pointers, whereas `#define IntPtr int *` would make `a` a pointer and `b` an `int`.

### A singly linked list

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct node {
    int data;
    struct node *next;
} Node;

Node *push_front(Node *head, int v)
{
    Node *n = malloc(sizeof *n);
    if (n == NULL)
        exit(EXIT_FAILURE);
    n->data = v;
    n->next = head;
    return n;
}

int main(void)
{
    Node *head = NULL;
    for (int i = 1; i <= 4; i++)
        head = push_front(head, i * 10);
    printf("list: ");
    for (Node *p = head; p != NULL; p = p->next)
        printf("%d -> ", p->data);
    printf("NULL\n");
    int total = 0;
    while (head != NULL) {
        Node *dead = head;
        total += head->data;
        head = head->next;
        free(dead);
    }
    printf("sum = %d, list freed\n", total);
    return 0;
}
```
```output
list: 40 -> 30 -> 20 -> 10 -> NULL
sum = 100, list freed
```

Each node is created with `malloc`, linked to the previous head, and finally released with `free`, saving `next` before the node is freed. Inserting at the front costs O(1), but reaching the *k*-th node costs O(k) because there is no indexing: that is the trade-off against an array.

### Table lookup

Many programs map a name to a value (a month name to its number, a command to its handler). A **table lookup** keeps an array of structures and searches it, either with a linear loop or, if sorted, with `bsearch`:

```c
#include <stdio.h>
#include <string.h>

struct entry { const char *name; int days; };

static const struct entry months[] = {
    {"Baisakh", 31}, {"Jestha", 31}, {"Asar", 32}, {"Shrawan", 31},
    {"Bhadra", 31}, {"Ashwin", 30}
};

int lookup(const char *name)
{
    for (size_t i = 0; i < sizeof months / sizeof months[0]; i++)
        if (strcmp(months[i].name, name) == 0)
            return months[i].days;
    return -1;
}

int main(void)
{
    printf("Asar has %d days\n", lookup("Asar"));
    printf("Poush has %d days\n", lookup("Poush"));
    return 0;
}
```
```output
Asar has 32 days
Poush has -1 days
```

(The day counts of Bikram Sambat months change from year to year; the numbers here only illustrate a table.)

## 8.6 Pointers to functions and callbacks

A function name is the address of its code, and a **pointer to a function** stores that address. The declaration `int (*op)(int, int);` reads "`op` is a pointer to a function taking two `int` and returning `int`"; the parentheses around `*op` are essential, because `int *op(int, int)` declares a function returning `int *`.

```c
#include <stdio.h>
#include <stdlib.h>

int add(int a, int b) { return a + b; }
int mul(int a, int b) { return a * b; }

int apply(int (*op)(int, int), int x, int y)
{
    return op(x, y);
}

int by_value_desc(const void *p, const void *q)
{
    return *(const int *)q - *(const int *)p;
}

int main(void)
{
    int (*table[2])(int, int) = {add, mul};
    printf("apply(add, 6, 7) = %d\n", apply(add, 6, 7));
    printf("apply(mul, 6, 7) = %d\n", apply(mul, 6, 7));
    printf("table[1](3, 4)   = %d\n", table[1](3, 4));
    int a[5] = {40, 10, 50, 30, 20};
    qsort(a, 5, sizeof a[0], by_value_desc);
    printf("sorted descending:");
    for (int i = 0; i < 5; i++)
        printf(" %d", a[i]);
    printf("\n");
    return 0;
}
```
```output
apply(add, 6, 7) = 13
apply(mul, 6, 7) = 42
table[1](3, 4)   = 12
sorted descending: 50 40 30 20 10
```

Passing a function to another function is a **callback**: `qsort` does not know how to compare your data, so you hand it a comparison function. An array of function pointers is a simple dispatch table (menu handlers, state machines). The same idea reappears as listeners in Java and callbacks in JavaScript.

## 8.7 Eight uses of the topics in this unit

1. **Include guards** in every header of a multi-file project.
2. **Named constants** and configuration switches (`#define BUFFER_SIZE 256`).
3. **Debug builds**: `#ifdef DEBUG` around trace output, removed in the release build with `gcc -DDEBUG` omitted.
4. **Portable code**: `#if defined(_WIN32)` for Windows-only code and `#else` for Linux.
5. **Permission and status flags** stored as bits of one integer (file permissions `rwx`).
6. **Command-line tools**: `grep`-like programs that read their input names from `argv`.
7. **Dynamic data structures**: linked lists, stacks and queues built from self-referential nodes.
8. **Callbacks and dispatch tables**: sorting with `qsort`, menu handlers, event loops.

## 8.8 Laboratory work: the course checklist

The TU outline lists lab work against its units. Each line below names a set of programs; finish all of them and keep the output as your journal.

| Outline units | Practical programs |
|---|---|
| 1 to 4 | data types and `sizeof` for each type; arithmetic, relational, logical, assignment, ternary, bitwise operators; operator precedence and associativity by evaluating mixed expressions; `printf`/`scanf` with width and precision; `getchar`/`putchar` |
| 5 | grade finder with `if`/`else if` ladder; calculator with `switch`; factorial, Fibonacci, prime test, digit sum, reverse number; pyramid patterns with nested loops; the same loop with `for`, `while` and `do while` |
| 6 | largest, smallest and sorted order of an array; matrix addition, multiplication and transpose; string length, copy, compare, concatenate and reverse with and without `<string.h>`; palindrome test |
| 7 | functions with and without parameters and return values; recursive factorial, GCD and Fibonacci; swap by value and by address; `static` counter, global and local variables |
| 8 | macros with arguments, `SQUARE` and `MAX`; a header file with an include guard; `#if`, `#ifdef`, `#ifndef`, `#else`, `#elif`; `gcc -E`, `-S`, `-c` to inspect each stage |
| 9 | pointer arithmetic over an array; pointers and strings; passing pointers to functions; `malloc`, `calloc`, `realloc`, `free` for a dynamic array |
| 10 | structure for a student; array of structures; nested structure; passing a structure and an array of structures to a function; pointer to structure; union demonstration; a file-based record store |

## Formula and fact sheet

- Macro arguments need parentheses: `#define SQ(x) ((x)*(x))`; never pass `i++` to a macro.
- `#` stringizes, `##` pastes tokens; `#if` needs a constant expression; always add include guards.
- Build stages: preprocess, compile, assemble, link, load. `undefined reference` is a link error.
- Masks: set `|=`, clear `&= ~`, toggle `^=`, test `>>` then `& 1`. `x & (x-1) == 0` means a power of two (or 0).
- `argv[0]` is the program name; `argc` counts it; arguments are strings.
- A self-referential structure holds a pointer to its own type; free each node after saving `next`.
- `int (*f)(int, int)` is a pointer to function; callbacks such as `qsort` take one.

## Chapter summary

- The preprocessor performs textual substitution before compilation; macros are fast but unchecked.
- A C program is built in five stages; errors belong to a stage.
- Bitwise operators manipulate individual bits; bit-fields pack small values.
- The odd loop, `exit` and `argc/argv` complete flow control and program interfaces.
- Self-referential structures give linked data; function pointers give callbacks.

## Practice

**A. Short questions**

1. Differentiate a macro and a function.
2. What is the purpose of `#ifndef`, `#define`, `#endif` in a header?
3. Name the stages of the C build process and the output of each.
4. What is the difference between `#include <file.h>` and `#include "file.h"`?
5. What does `x & (x - 1)` do?
6. What are `argc` and `argv`?
7. What is a self-referential structure?
8. Explain `int (*p)(int);`.

**B. Predict**

9. `#define CUBE(x) x*x*x` → value of `CUBE(1+2)`.
10. `int x = (4, 7, 9);` → value of `x`.
11. `printf("%d", 13 & 6);`, `printf("%d", 13 | 6);`, `printf("%d", 13 ^ 6);`
12. `printf("%d", 5 << 3);` and `printf("%d", 100 >> 2);`

**C. Programs**

13. Write macros `MIN`, `MAX` and `ABS` and test them with a header file.
14. Write a program that prints the bits of an `unsigned` number.
15. Write a program that adds all numbers given on the command line.
16. Build a linked list of student names and marks, print it, and delete the node with a given roll number.
17. Write a menu-driven program that uses an array of function pointers.

::: note Answers and worked solutions
**1.** A macro is replaced by text before compilation, with no type check and possible repeated evaluation of arguments; a function is compiled once, called at run time, and has typed parameters.
**2.** The include guard stops the declarations being processed twice when the header is included from several files.
**3.** Preprocessing gives expanded source (`.i`), compiling gives assembly (`.s`), assembling gives an object file (`.o`), linking gives the executable, and loading places it in memory.
**4.** The angle form searches the system include directories; the quote form searches the current directory first.
**5.** It clears the lowest set bit of `x`; the result is 0 if `x` is a power of two.
**6.** `argc` counts the command-line words (including the program name); `argv` is the array of those words as strings.
**7.** A structure that contains a pointer to a structure of its own type, used to build lists and trees.
**8.** `p` is a pointer to a function that takes an `int` and returns an `int`.
**9.** `1+2*1+2*1+2 = 7`, not 27.
**10.** 9 (the last operand of the comma expression).
**11.** 13 = 1101, 6 = 0110, so AND = 0100 = 4, OR = 1111 = 15, XOR = 1011 = 11.
**12.** `5 << 3 = 40` and `100 >> 2 = 25`.
**13.** `#define MIN(a,b) ((a)<(b)?(a):(b))` and similarly for the others, placed inside `#ifndef ... #endif`.
**14.** Loop `i` from 31 down to 0 and print `(x >> i) & 1`.
**15.** Loop `i` from 1 to `argc - 1` and add `atoi(argv[i])`; print a usage line when `argc == 1`.
**16.** Use a node with `roll`, `name`, `marks`, `next`; to delete, keep a `prev` pointer, relink `prev->next = cur->next` (or move the head), then `free(cur)`.
**17.** Declare `void (*menu[3])(void) = {add_rec, show_rec, quit};` and call `menu[choice - 1]()` after range-checking `choice`.
:::

## Model answers: medium (5 marks) and long (10 marks) questions

**Q (5 marks). Explain the C build process.**

A C program is converted into a running program in five stages. (1) **Preprocessing** handles directives: `#include` files are pasted, macros are expanded, comments are removed and conditional code is selected. (2) **Compiling** checks syntax and types and translates the code to assembly language. (3) **Assembling** translates assembly to machine code in an object file. (4) **Linking** combines object files and library functions such as `printf` into one executable and resolves all references; a missing function gives an *undefined reference* error. (5) **Loading** is done by the operating system, which copies the executable into memory and starts `main`.

**Q (5 marks). Distinguish macros and functions. Why must macro arguments be parenthesised?**

Macros are expanded by the preprocessor, so there is no call overhead, but code is repeated at every use, there is no type checking and an argument with a side effect may be evaluated twice. Functions are compiled once, type-checked and called at run time. Parentheses are needed because a macro only substitutes text: with `#define SQ(x) x*x`, `SQ(2+3)` becomes `2+3*2+3 = 11`; with `#define SQ(x) ((x)*(x))` it is `25` as intended.

**Q (10 marks). Write a program using a self-referential structure to create a linked list of integers, display it and free it. Explain each part.**

Use the program of section 8.5: `struct node` holds `data` and `next`; `push_front` allocates a node with `malloc`, checks for `NULL`, stores the value, makes `next` point to the old head, and returns the new head. The driver builds the list `40 -> 30 -> 20 -> 10 -> NULL`, traverses it with `for (p = head; p != NULL; p = p->next)`, and frees each node after saving the `next` pointer, so no memory leaks. Mention that insertion at the front is O(1) while access to the *k*-th node is O(k), and that forgetting to save `next` before `free` is a classic bug.
