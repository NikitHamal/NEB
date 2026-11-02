---
subject: Programming in C
grade: BCA Semester 1
unit: 6
title: Pointers and Dynamic Memory Allocation
hours: 6
area: BCA 102 · Programming in C · Unit 8
---

Every variable lives at an address in memory. A **pointer** is a variable that stores such an address. Pointers are the feature that makes C powerful and the feature that makes C dangerous; once they click, arrays, strings, linked lists and file buffers all become the same idea.

::: key What this unit gives you
- `&` (address-of) and `*` (dereference); declaring and initialising pointers.
- Pointer arithmetic and the array–pointer relationship.
- Pointers and strings, arrays of pointers, pointer to pointer.
- Pointers as function arguments and returned from functions.
- `malloc`, `calloc`, `realloc`, `free`, and the bugs they invite.
:::

## 6.1 Addresses, pointers and the two operators

```c
#include <stdio.h>

int main(void)
{
    int x = 10;
    int *p = &x;
    printf("x=%d *p=%d\n", x, *p);
    *p = 25;
    printf("x=%d\n", x);
    int **pp = &p;
    **pp += 5;
    printf("x=%d, p points to x: %d, pp points to p: %d\n", x, p == &x, pp == &p);
    printf("sizeof(p)=%zu sizeof(int)=%zu\n", sizeof(p), sizeof(int));
    return 0;
}
```
```output
x=10 *p=10
x=25
x=30, p points to x: 1, pp points to p: 1
sizeof(p)=8 sizeof(int)=4
```

- `int *p;` declares `p` as "pointer to int". `&x` is the address of `x`. `*p` (dereference) is *the object `p` points to*, usable on both sides of `=`.
- A pointer holds an address (8 bytes on a 64-bit system, whatever it points to; 2 bytes in 16-bit Turbo C near pointers).
- `int **pp` is a **pointer to pointer** (chain of pointers): `**pp` is `x`.
- An **uninitialised** pointer holds garbage; dereferencing it crashes. Set unused pointers to `NULL` (address 0) and test before use. Dereferencing `NULL` is undefined (a segmentation fault in practice).
- `void *` is a generic pointer: it can hold any address but must be cast before dereferencing.

**Advantages:** efficient array and string handling, functions that modify caller data, dynamic memory, data structures. **Disadvantages:** easy to misuse (dangling, wild, NULL pointers), hard-to-find bugs, security holes.

## 6.2 Pointer arithmetic

Adding *k* to a pointer moves it by *k elements*, not *k bytes*: `p + k` is the address `p + k × sizeof(*p)`. Subtracting two pointers into the same array gives the number of elements between them. Allowed: `p + n`, `p − n`, `p++`, `p − q`, comparisons. Not allowed: adding two pointers, multiplying or dividing a pointer.

For `int a[5]` with 4-byte `int` and `a` at address 2000: `a + 1` is 2004, `a + 3` is 2012, and `*(a + 3)` is `a[3]`.

**Arrays and pointers.** In most expressions an array name is the address of its first element, so `a[i]` is defined as `*(a + i)`. That is why `i[a]` also compiles. Differences: an array name is *not a variable* (you cannot do `a++` or `a = p`), and `sizeof(a)` gives the whole array while `sizeof(p)` gives only a pointer.

```c
#include <stdio.h>

int main(void)
{
    int a[5] = {10, 20, 30, 40, 50};
    int *p = a;
    printf("%d %d %d\n", *p, *(p + 2), p[4]);
    p += 3;
    printf("%d offset=%ld\n", *p, (long)(p - a));
    p--;
    printf("%d\n", *p);
    int sum = 0;
    for (int *q = a; q < a + 5; q++)
        sum += *q;
    printf("sum=%d\n", sum);
    printf("*a+1=%d  *(a+1)=%d\n", *a + 1, *(a + 1));
    return 0;
}
```
```output
10 30 50
40 offset=3
30
sum=150
*a+1=11  *(a+1)=20
```

After `p += 3`, `p` points at `a[3]`, so `*p` is 40 and `p - a` is 3; `p--` steps back to `a[2]`. Note that `*a + 1` is `(*a) + 1` because unary `*` binds tighter than `+`. Do not put `*p` and `*--p` in the same call: C does not say which argument is evaluated first.

## 6.3 Pointers and strings

A string can be handled through a `char *`. Two different things look similar:

- `char s[] = "Nepal";` is an **array** holding a *copy* of the text; you may modify it.
- `char *p = "Nepal";` points to a **string literal** in read-only memory; modifying it is undefined.

```c
#include <stdio.h>

int length(const char *s)
{
    const char *start = s;
    while (*s)
        s++;
    return (int)(s - start);
}

void copy(char *dst, const char *src)
{
    while ((*dst++ = *src++))
        ;
}

int main(void)
{
    char a[20];
    copy(a, "Pokhara");
    printf("%s has %d letters\n", a, length(a));
    const char *cities[] = {"Kathmandu", "Pokhara", "Biratnagar"};
    for (int i = 0; i < 3; i++)
        printf("%s(%d) ", cities[i], length(cities[i]));
    printf("\n%c %c\n", cities[1][0], *(*(cities + 2) + 3));
    return 0;
}
```
```output
Pokhara has 7 letters
Kathmandu(9) Pokhara(7) Biratnagar(10) 
P a
```

`cities` is an **array of pointers** to strings: each element points to its own literal, so the strings need not be the same length (unlike a 2-D `char` array, which wastes space). `*(*(cities + 2) + 3)` is the 4th character of the 3rd string: `a` in "Biratnagar" (B-i-r-**a**).

`copy` shows the idiom `while ((*dst++ = *src++));`: copy a character, advance both, and stop after copying `'\0'` (value 0 = false).

## 6.4 Pointers and functions

1. **Pointer parameters** let a function modify the caller's data (Unit 5's `swap`) and return several results.
2. **Passing arrays**: `void f(int *a, int n)` and `void f(int a[], int n)` are identical.
3. **`const`** documents and enforces read-only access: `const char *s` means "I will not change the characters".
4. **Returning a pointer**: legal, but *never return the address of a local variable*; it dies when the function returns (a **dangling pointer**). Return a pointer to `static` storage, to memory from `malloc`, or to something the caller owns.
5. **Function pointers** (`int (*op)(int, int)`) let you choose a function at run time; they power callbacks like `qsort`.

## 6.5 Dynamic memory allocation

Local variables live on the **stack** and vanish at block exit; array sizes must be known at compile time. **Dynamic allocation** takes memory from the **heap** at run time, in an amount you choose, and keeps it until you release it. Header: `<stdlib.h>`.

| Function | Effect |
|---|---|
| `malloc(bytes)` | allocates `bytes` uninitialised bytes; returns `NULL` on failure |
| `calloc(n, size)` | allocates `n × size` bytes **zeroed** |
| `realloc(p, newbytes)` | resizes a block, possibly moving it; may return `NULL` (then the old block is still valid) |
| `free(p)` | returns the block to the heap |

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int n = 5;
    int *a = malloc(n * sizeof *a);
    if (a == NULL) {
        printf("out of memory\n");
        return 1;
    }
    for (int i = 0; i < n; i++)
        a[i] = (i + 1) * (i + 1);
    int *tmp = realloc(a, 8 * sizeof *a);
    if (tmp == NULL) {
        free(a);
        return 1;
    }
    a = tmp;
    for (int i = n; i < 8; i++)
        a[i] = 0;
    for (int i = 0; i < 8; i++)
        printf("%d ", a[i]);
    printf("\n");
    free(a);
    a = NULL;

    int *z = calloc(4, sizeof(int));
    printf("calloc: %d %d %d %d\n", z[0], z[1], z[2], z[3]);
    free(z);
    return 0;
}
```
```output
1 4 9 16 25 0 0 0 
calloc: 0 0 0 0
```

`malloc(n * sizeof *a)` is the safest spelling: it stays correct if the type of `a` changes. Do not cast the result of `malloc` in C. Always check for `NULL`.

**The bugs** — memorise the list, examiners ask for it:

| Bug | Meaning |
|---|---|
| **Memory leak** | allocated, never freed; a long-running program slowly eats RAM |
| **Dangling pointer** | using a pointer after `free` or after its variable died |
| **Double free** | calling `free` twice on the same block |
| **Buffer overflow** | writing beyond the allocated size |
| **Use of uninitialised pointer** | wild pointer; set pointers to `NULL` |
| **Freeing non-heap memory** | `free(&x)` or `free(p + 1)` |

Rule: every `malloc` has exactly one `free`; set the pointer to `NULL` afterwards. A **2-D array** can be made by allocating an array of row pointers and then each row.

## Formula and fact sheet

- `&x` address of x; `*p` object at p; `p == &x` means p points to x.
- `p + k` moves k *elements*; `a[i] ≡ *(a + i)`; `p - q` counts elements.
- Pointer size is the same for every pointer type (8 bytes on 64-bit).
- `char s[] = "…"` copy, modifiable; `char *p = "…"` literal, read-only.
- Never return a pointer to a local. `malloc`/`calloc`/`realloc` → check `NULL` → `free` once.

## Chapter summary

- A pointer is an address with a type; `*` follows it, `&` makes it.
- Array indexing is pointer arithmetic in disguise.
- Strings are `char` sequences handled by pointer; arrays of pointers store ragged lists.
- The heap gives size flexibility at the price of discipline: allocate, check, use, free.

## Practice

**A. Short questions**

1. Differentiate `*p` in a declaration and `*p` in an expression.
2. If `int a[] = {5, 10, 15}` and `int *p = a;`, what are `*p`, `*(p+1)`, `p[2]`, `*p + 1`?
3. What is a dangling pointer? Give an example.
4. Differentiate `malloc` and `calloc`. Why must the result be checked?
5. State three differences between an array name and a pointer variable.
6. What is wrong with `char *s = "abc"; s[0] = 'x';`?

**B. Predict**

7. `int x = 4, y = 9; int *p = &x, *q = &y; *p = *q; *q = 1; printf("%d %d", x, y);`
8. `int a[4] = {1,2,3,4}; int *p = a + 3; printf("%d %ld", *p, p - a);`

**C. Programs**

9. Write `void reverse(char *s)` that reverses a string in place using two pointers.
10. Read n, allocate an array dynamically, read n numbers, print the largest, free the memory.
11. Write a function that returns a pointer to the largest element of an array (return `NULL` for n = 0).
12. Find and fix: `int *f(void){ int v = 3; return &v; }`

::: note Answers and worked solutions
**1.** In a declaration `*` says "p is a pointer"; in an expression `*` is the dereference operator giving the pointed-to object.
**2.** 5, 10, 15, 6.
**3.** A pointer holding the address of memory that no longer belongs to the program, e.g. `free(p);` followed by `*p`, or a pointer to a local variable returned from a function.
**4.** `malloc` leaves memory uninitialised; `calloc` zeroes it and takes a count and a size. Both return `NULL` on failure; using that result crashes.
**5.** An array name is a constant address (no `a++`, no `a = p`); `sizeof(a)` is the whole array, `sizeof(p)` is the pointer; the array owns its storage while the pointer only refers to storage.
**6.** The literal is in read-only memory; modifying it is undefined (usually a crash). Use `char s[] = "abc";`.
**7.** `x` becomes 9, then `y` becomes 1: output `9 1`.
**8.** `4 3`.
**9.** `void reverse(char *s){ char *e = s; while (*e) e++; e--; while (s < e){ char t = *s; *s++ = *e; *e-- = t; } }`
**10.** `int *a = malloc(n * sizeof *a); … int max = a[0]; for (i = 1; i < n; i++) if (a[i] > max) max = a[i]; printf("%d", max); free(a);`
**11.** `int *largest(int *a, int n){ if (n == 0) return NULL; int *m = a; for (int i = 1; i < n; i++) if (a[i] > *m) m = &a[i]; return m; }`
**12.** `v` dies when `f` returns. Make it `static int v = 3;`, or allocate with `malloc`, or have the caller pass the address to fill.
:::
