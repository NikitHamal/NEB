---
subject: Programming in C
grade: BCA Semester 1
unit: 7
title: Structures, Unions and File Handling
hours: 9
area: BCA 102 · Programming in C · Units 9 and 10
---

Arrays hold many values of the *same* type. Real records (a student with a name, a roll number and marks) mix types, so C offers the **structure**. And because variables vanish when the program ends, **files** let data survive. These two ideas together are the smallest database.

::: key What this unit gives you
- Structures: declaration, initialisation, access with `.` and `->`, arrays of structures, nesting, passing to functions, `typedef`.
- Unions and how they differ from structures (size, memory, use).
- `enum` and the preprocessor basics (`#define`, macros, `#include`, conditional compilation).
- Text and binary files: modes, `fopen`/`fclose`, `fprintf`/`fscanf`, `fgets`/`fputs`, `fread`/`fwrite`, `fseek`/`ftell`/`rewind`, error checking.
:::

## 7.1 Structures

```c
struct student {
    int roll;
    char name[30];
    float marks;
};
```

This declares a new *type* `struct student` and reserves no memory. Create variables with `struct student s1, s2;`. Initialise with braces in member order: `struct student s1 = {1, "Asha", 82.5f};`. C99 also allows designated initialisers: `{.name = "Asha", .roll = 1}`.

Members are accessed with the **dot** operator on a structure and the **arrow** operator on a pointer to a structure: `s1.roll`, `ps->roll` (which is shorthand for `(*ps).roll`). Assigning one structure to another of the same type (`s2 = s1;`) copies every member, **including arrays inside it**; arrays on their own cannot be assigned. Structures cannot be compared with `==`; compare members.

`typedef struct student Student;` (or `typedef struct { … } Student;`) lets you write `Student s1;` without the word `struct`.

**Memory layout and padding.** Members are stored in declaration order, but the compiler inserts *padding* so each member sits at an address suitable for its type. `struct { char c; int i; }` is typically 8 bytes, not 5: 1 byte for `c`, 3 bytes padding, 4 for `i`. Ordering members from largest to smallest reduces padding. Always use `sizeof(struct …)`, never add member sizes by hand.

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    int roll;
    char name[20];
    float marks;
} Student;

struct date { int d, m, y; };
struct person { char name[20]; struct date dob; };

void print(const Student *s)
{
    printf("%d %-6s %.1f\n", s->roll, s->name, s->marks);
}

int main(void)
{
    Student cls[3] = {{1, "Asha", 82.5f}, {2, "Bikash", 67.0f}, {3, "Sita", 91.25f}};
    int best = 0;
    for (int i = 1; i < 3; i++)
        if (cls[i].marks > cls[best].marks)
            best = i;
    printf("topper: ");
    print(&cls[best]);

    for (int i = 0; i < 2; i++)
        for (int j = 0; j < 2 - i; j++)
            if (cls[j].marks < cls[j + 1].marks) {
                Student t = cls[j];
                cls[j] = cls[j + 1];
                cls[j + 1] = t;
            }
    for (int i = 0; i < 3; i++)
        print(&cls[i]);

    struct person p = {"Ram", {14, 4, 2005}};
    printf("%s was born in %d\n", p.name, p.dob.y);
    printf("sizeof(Student)=%zu\n", sizeof(Student));
    return 0;
}
```
```output
topper: 3 Sita   91.2
3 Sita   91.2
1 Asha   82.5
2 Bikash 67.0
Ram was born in 2005
sizeof(Student)=28
```

(91.25 prints as 91.2 because `%.1f` rounds the binary value half to even; the size 28 = 4 + 20 + 4 with no padding needed here.)

Passing a structure to a function **by value** copies all of it; for anything bigger than a couple of members pass a pointer (`const Student *s`) as `print` does. An **array of structures** is a table; sorting it swaps whole records. **Nested structures** model "has-a" relations (`p.dob.y`). **Self-referential** structures hold a pointer to their own type and form linked lists: `struct node { int data; struct node *next; };`.

## 7.2 Unions and enumerations

A **union** declares members that all share the *same* memory. Its size is that of the largest member, and only one member holds a valid value at a time (the last one written).

| Structure | Union |
|---|---|
| each member has its own memory | all members share one block |
| size ≥ sum of members (plus padding) | size = largest member (plus padding) |
| all members usable together | only the last-written member is meaningful |
| keyword `struct` | keyword `union` |
| use: records | use: saving memory, variant data, viewing the same bytes in two ways |

```c
#include <stdio.h>

union value {
    int i;
    float f;
    char c;
};

enum day { SUN, MON, TUE, WED = 10, THU };

int main(void)
{
    union value v;
    v.i = 65;
    printf("as int=%d as char=%c\n", v.i, v.c);
    v.f = 1.5f;
    printf("size=%zu\n", sizeof(union value));
    printf("%d %d %d %d\n", SUN, TUE, WED, THU);
    return 0;
}
```
```output
as int=65 as char=A
size=4
0 2 10 11
```

An **enum** names integer constants: values start at 0 and increase by 1 unless set. Here SUN is 0, MON 1, TUE 2, WED is set to 10, so THU is 11 (third output line). In the union, writing `v.f` after `v.i` overwrote the same four bytes, so only the last-written member is meaningful.

## 7.3 The preprocessor in brief

Lines starting with `#` are handled *before* compilation.

| Directive | Meaning |
|---|---|
| `#include <f.h>` / `"f.h"` | paste a header (system path / local first) |
| `#define N 100` | object-like macro: replace `N` by `100` |
| `#define SQ(x) ((x)*(x))` | function-like macro: parenthesise every argument and the whole body |
| `#undef N` | forget the macro |
| `#ifdef X … #endif`, `#ifndef`, `#if`, `#else` | conditional compilation |
| *include guard* | `#ifndef MYH` / `#define MYH` / … / `#endif` stops a header being included twice |

A macro is textual substitution: `SQ(i++)` expands to `((i++)*(i++))`, which modifies `i` twice (undefined). A function is safer; macros win only for tiny, type-generic expressions.

## 7.4 Files

A file is a named sequence of bytes on disk. A `FILE *` (from `<stdio.h>`) is the handle.

```text
FILE *fp = fopen("data.txt", "w");
if (fp == NULL) { perror("open"); return 1; }
...
fclose(fp);
```

| Mode | Meaning |
|---|---|
| `"r"` | read; the file must exist |
| `"w"` | write; **creates or truncates** (destroys old content) |
| `"a"` | append at the end; creates if missing |
| `"r+"` | read and write; the file must exist |
| `"w+"` | read and write; truncates |
| `"a+"` | read and append |
| add `b` | binary mode: `"rb"`, `"wb"`, `"ab"` (matters on Windows, where text mode translates `\n`) |

Always test `fopen` against `NULL`, and always `fclose` (it flushes the buffer; data not flushed can be lost).

**Text files** (readable characters): `fprintf(fp, "%d %s\n", n, s)` writes formatted; `fscanf(fp, "%d", &n)` reads formatted and returns the number of items read; `fgets(buf, size, fp)` reads a line and returns `NULL` at end of file; `fputs`, `fgetc`, `fputc` do lines and characters. **Never loop on `feof`** alone; test the return value of the read call (the classic bug is processing the last record twice).

**Binary files** (raw bytes): `fwrite(&rec, sizeof rec, 1, fp)` writes one record exactly as it is in memory; `fread(&rec, sizeof rec, 1, fp)` reads it back and returns the number of records read. Binary records have fixed size, which is what makes random access possible.

**Random access**: `fseek(fp, offset, origin)` with origin `SEEK_SET` (start), `SEEK_CUR` or `SEEK_END`; `ftell(fp)` reports the position; `rewind(fp)` returns to the start. To read record number *k* (0-based): `fseek(fp, k * sizeof(Student), SEEK_SET)`.

```c
#include <stdio.h>

typedef struct { int roll; char name[16]; float marks; } Rec;

int main(void)
{
    FILE *fp = fopen("marks.dat", "wb");
    if (fp == NULL)
        return 1;
    Rec in[3] = {{1, "Asha", 82.5f}, {2, "Bikash", 67.0f}, {3, "Sita", 91.0f}};
    fwrite(in, sizeof(Rec), 3, fp);
    fclose(fp);

    fp = fopen("marks.dat", "rb");
    if (fp == NULL)
        return 1;
    fseek(fp, 0, SEEK_END);
    long bytes = ftell(fp);
    printf("file size=%ld bytes = %ld records\n", bytes, bytes / (long)sizeof(Rec));
    fseek(fp, 1 * sizeof(Rec), SEEK_SET);
    Rec r;
    if (fread(&r, sizeof r, 1, fp) == 1)
        printf("record 1: %d %s %.1f\n", r.roll, r.name, r.marks);
    fclose(fp);

    fp = fopen("notes.txt", "w");
    fprintf(fp, "10 20 30\nBCA\n");
    fclose(fp);
    fp = fopen("notes.txt", "r");
    int a, b, c, sum = 0;
    if (fscanf(fp, "%d %d %d", &a, &b, &c) == 3)
        sum = a + b + c;
    char word[10];
    fscanf(fp, "%9s", word);
    fclose(fp);
    printf("sum=%d word=%s\n", sum, word);

    fp = fopen("missing.txt", "r");
    printf("missing.txt opened: %s\n", fp ? "yes" : "no");
    return 0;
}
```
```output
file size=72 bytes = 3 records
record 1: 2 Bikash 67.0
sum=60 word=BCA
missing.txt opened: no
```

Here `Rec` is 24 bytes (4 + 16 + 4), so three records occupy 72 bytes, and `fseek(fp, 1 * sizeof(Rec), SEEK_SET)` lands exactly on the second record. A **text-file append, search, update** program uses `"a"`, reads sequentially comparing keys, and for updates uses a binary file with `fseek` back by one record before `fwrite`. **Command-line arguments** (`argc`, `argv`) let a program receive file names: `./copy a.txt b.txt`.

::: caution File traps
Opening with `"w"` erases the file. Mixing reads and writes on a `"r+"` stream needs an `fseek` or `fflush` between them. Writing a structure that contains a pointer to a binary file stores the *address*, not the pointed-to data. Binary files are not portable between machines with different sizes or byte orders.
:::

## Formula and fact sheet

- `.` for a structure variable, `->` for a pointer to a structure; `s2 = s1` copies everything.
- Struct size ≥ sum of members (padding); union size = largest member.
- Modes: `r w a r+ w+ a+` and `b`; `w` truncates.
- `fwrite(&x, sizeof x, count, fp)`; `fseek(fp, k * sizeof rec, SEEK_SET)` finds record k.
- Loop on the return value of `fscanf`/`fgets`/`fread`, not on `feof`.

## Chapter summary

- A structure groups different types into one record; arrays of structures are tables.
- A union overlays members in one block; an enum names integers.
- Preprocessor lines run before compilation; parenthesise macros.
- Files make data permanent: open, check, read or write, close; binary files plus `fseek` give random access.

## Practice

**A. Short questions**

1. Differentiate structure and union with an example of each.
2. Why can a structure be larger than the sum of its members?
3. When do you use `.` and when `->`?
4. Distinguish text and binary files. Which functions suit each?
5. What is the difference between modes `"w"`, `"a"` and `"r+"`?
6. What is `#ifndef` / `#define` / `#endif` at the top of a header for?

**B. Predict**

7. `union u { int i; char c[4]; }; printf("%zu", sizeof(union u));` (4-byte int)
8. `struct s { char c; int i; }; printf("%zu", sizeof(struct s));` on a typical 64-bit compiler.
9. `#define SQ(x) x*x` → value of `SQ(2+3)`.

**C. Programs**

10. Define a structure for an employee (id, name, salary); read n employees and print the one with the highest salary.
11. Write a program that copies a text file to another, character by character.
12. Count the number of lines, words and characters in a text file.
13. Store records in a binary file and write a function to update the marks of the record with a given roll number.

::: note Answers and worked solutions
**1.** A `struct` gives each member its own storage: `struct {int a; float b;}` is at least 8 bytes. A `union` shares storage: `union {int a; float b;}` is 4 bytes and holds one value at a time.
**2.** The compiler pads members to alignment boundaries so each is accessed efficiently.
**3.** `.` with a structure variable (`s.roll`); `->` with a pointer to a structure (`p->roll`).
**4.** Text files store characters (human-readable, line-oriented); use `fprintf`, `fscanf`, `fgets`, `fputs`. Binary files store raw memory images in fixed-size records; use `fread`, `fwrite`, `fseek`.
**5.** `"w"` creates or empties the file for writing; `"a"` appends at the end, keeping content; `"r+"` reads and writes an existing file without truncating it.
**6.** An include guard: it prevents the header's declarations from being processed twice if it is included more than once, which would cause redefinition errors.
**7.** 4 (the members overlap).
**8.** 8 (1 byte, 3 padding, 4 for the int).
**9.** `2+3*2+3 = 11`, not 25. Define it as `((x)*(x))`.
**10.** Read into `struct emp e[n]`; keep an index `best` updated when `e[i].salary > e[best].salary`; print `e[best]`.
**11.** `while ((ch = fgetc(in)) != EOF) fputc(ch, out);` with `int ch`, and both files checked for `NULL` and closed.
**12.** Loop over characters: every `'\n'` adds a line; a word starts when a non-space follows a space; every character adds to the count.
**13.** Open with `"rb+"`; read records until `rec.roll == key`; `fseek(fp, -(long)sizeof rec, SEEK_CUR)`; change the marks; `fwrite` the record back; close.
:::
