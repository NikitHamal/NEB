---
file: NEBians-IOE-Past-Paper-Computer-Programming-CT401-2081-Baishakh.pdf
subject: Computer Programming
level: BE · Year I / Part I
code: CT 401
year_bs: 2081 Baishakh
cal: BS
year_ad: 2024
stream: All programmes except B.Arch and BAS
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, CT 401). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Discuss about compilation process in C. Draw a flowchart to calculate the sum of digits contained in a number entered by the user. [[4+4]]

@q 2
Explain about declaring variables and constants in C and FORTRAN. [[4+4]]

@q 3
Write a syntax to use else-if ladder and do-while in C. Write a program in C to generate the given pattern using concept of loop control. [[2+4]]

```text
          1
       2  4
    3  6  9
 4  8  12 16
```

@q 4
Write a program using recursive function to compute $x^y$ and explain how this program works. [[4+4]]

@q 5
Explain about `toupper()` and `tolower()` function used in C. Write a C program to read the name of $N$ countries and display the name of these countries in alphabetical order. [[2+6]]

@q 6
Discuss about the initialization and declaration of pointers with examples. Write down about pointer arithmetic. [[2+6]]

@q 7
Write a program in C (16-bit compiler) to create a structure name "karmachari" with members: ID_Number (6-digit), Name and salary of 40,000 employees. Create a function name `search()`. Where, the user inputs a value of salary within the records, if found display the records. [[8]]

@q 8
Write a program in C to write all the prime numbers within the range n1 to n2 into a first file, copy the content of first file into second file and display the content of second file. Your first file name should be "Source" and second file name should be "Destination". [[8]]

@q 9
Write a program in FORTRAN to display Fibonacci sequence upto $n^{th}$ term. Read $n$ from the user. [Fibonacci sequence: 0, 1, 1, 2, 3, 5, 8, 13, ...] [[8]]

@q 10
Compare switch statement with user defined function. Write a program in C to find the transpose of $N\times N$ matrix. [[3+5]]
<!-- SOLUTIONS -->
@s 1
**Compilation process in C.** A C source file (`prog.c`) becomes an executable program in four stages, run one after the other by the compiler driver (`gcc`, Turbo C):

```figure caption="Question 1(a): stages of the compilation process of a C program."
fig,ax=plt.subplots(figsize=(6.4,2.0)); ax.axis('off'); ax.set_xlim(0,16); ax.set_ylim(0,4)
st=[('Source\nfile','#fff3e0','#b8860b'),('Pre-\nprocessor','#e8eef7','#1d6fb8'),('Compiler','#e8eef7','#1d6fb8'),('Assembler','#e8eef7','#1d6fb8'),('Linker','#e8eef7','#1d6fb8'),('Executable\nfile','#e0f0e6','#2e8b57')]
lab=['expanded\nsource (.i)','assembly\n(.s)','object\ncode (.obj)','libraries\n(.lib)']
for i,(t,f,e) in enumerate(st):
    x=0.1+i*2.65
    ax.add_patch(plt.Rectangle((x,1.6),2.1,1.1,fc=f,ec=e,lw=1.2)); ax.text(x+1.05,2.15,t,ha='center',va='center',fontsize=6.8)
    if i<5: ax.annotate('',xy=(x+2.65,2.15),xytext=(x+2.1,2.15),arrowprops=dict(arrowstyle='->'))
for i,l in enumerate(lab):
    ax.text(0.1+i*2.65+2.4+1.3-0.3,1.0,l,ha='center',fontsize=6.5,color='#d9534f')
```

1. **Preprocessing:** the preprocessor handles the lines beginning with `#`: it includes the header files (`#include`), expands macros (`#define`), performs conditional compilation (`#ifdef`) and removes comments.
2. **Compilation:** the compiler checks the **syntax**, reports errors and warnings, and translates the preprocessed code into **assembly language** (and then machine-level object code).
3. **Assembling:** the assembler converts the assembly code into **relocatable machine code**, the object file (`prog.obj` / `prog.o`).
4. **Linking:** the linker combines the object file with the **library functions** (such as `printf()` from the standard library) and other object files and resolves the external references, producing the **executable file**.
5. **Loading and execution:** the loader brings the executable into memory and the CPU executes it. Errors found at each stage: syntax errors (compile time), linker errors (undefined function), runtime errors and logical errors.

**Flowchart for the sum of the digits of a number.**

*Algorithm:* read $n$; set sum $= 0$; while $n>0$: digit $= n \bmod 10$, sum $=$ sum $+$ digit, $n = n/10$ (integer division); print sum.

```figure caption="Question 1(b): flowchart for the sum of the digits of a number."
fig, ax = plt.subplots(figsize=(4.8, 4.8))
def B(x, y, t, k='p', w=2.4, h=0.7):
    if k == 'd':
        ax.add_patch(plt.Polygon([[x, y+h*0.8], [x+w*0.62, y], [x, y-h*0.8], [x-w*0.62, y]], fc='#fff3e0', ec='#b8860b'))
    elif k == 't':
        ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, fc='#e0f0e6', ec='#2e8b57', lw=1.6))
    elif k == 'io':
        ax.add_patch(plt.Polygon([[x-w/2+0.2, y+h/2], [x+w/2+0.2, y+h/2], [x+w/2-0.2, y-h/2], [x-w/2-0.2, y-h/2]], fc='#e8eef7', ec='#1d6fb8'))
    else:
        ax.add_patch(plt.Rectangle((x-w/2, y-h/2), w, h, fc='#e8eef7', ec='#1d6fb8'))
    ax.text(x, y, t, ha='center', va='center', fontsize=7.5)
def A(x1, y1, x2, y2, l=''):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color='#14181f', lw=1))
    if l:
        ax.text((x1+x2)/2+0.12, (y1+y2)/2+0.1, l, fontsize=7, color='#d9534f')
def L(xs, ys):
    ax.plot(xs, ys, color='#14181f', lw=1)
B(0,9.2,'Start','t'); A(0,8.85,0,8.5)
B(0,8.1,'Read n','io'); A(0,7.75,0,7.4)
B(0,7.0,'sum = 0'); A(0,6.65,0,6.25)
B(0,5.5,'n > 0 ?','d',w=2.2); A(0.7,5.5,1.9,5.5,'Yes'); A(0,4.9,0,4.2,'No')
B(3.4,5.5,'d = n % 10\nsum = sum + d\nn = n / 10',w=2.4,h=1.0)
L([3.4,3.4],[6.0,6.25]); L([3.4,0],[6.25,6.25])
B(0,3.8,'Print sum','io'); A(0,3.45,0,2.8)
B(0,2.45,'Stop','t')
ax.set_xlim(-2, 6.8); ax.set_ylim(2.0, 9.6); ax.axis('off')
```

For $n = 4825$: $5+2+8+4 = 19$. Program:

```c
#include <stdio.h>

int main(void)
{
    long n, temp;
    int sum = 0;

    printf("Enter a number: ");
    scanf("%ld", &n);
    temp = n;
    if (temp < 0)
        temp = -temp;
    while (temp > 0) {
        sum += temp % 10;      /* last digit */
        temp /= 10;            /* drop the last digit */
    }
    printf("Sum of digits of %ld = %d\n", n, sum);
    return 0;
}
```

Output: `Sum of digits of 4825 = 19`.

@s 2
**Variables.** A variable is a named memory location whose value can change during execution.

*In C* a variable must be **declared before use** by giving its data type and name (and it can be initialised in the declaration): `data_type name1, name2 = value;`. The name consists of letters, digits and underscore, must not start with a digit, must not be a keyword, and is case-sensitive. Types: `int`, `float`, `double`, `char`, etc. Variables are declared at the start of a block (inside functions: local; outside: global), with storage classes `auto`, `static`, `extern`, `register`.

*In FORTRAN* a variable name has at most 6 characters (FORTRAN 77), starts with a letter, and is typed by an explicit declaration `INTEGER COUNT`, `REAL RADIUS, AREA`, `CHARACTER*10 NAME`, `LOGICAL FLAG`, `DOUBLE PRECISION X`, or **implicitly** by the first letter (names starting with I, J, K, L, M, N are INTEGER, all others REAL, unless `IMPLICIT NONE` is used).

**Constants.** A constant is a fixed value that does not change during the execution.

*In C:* (i) literal constants: integer `25`, real `3.14`, character `'A'`, string `"Nepal"`; (ii) the **`const` qualifier**: `const int MAXN = 100;` (read-only variable); (iii) the **symbolic constant** with the preprocessor: `#define PI 3.14159`; (iv) enumeration constants: `enum {RED, GREEN, BLUE};`.

*In FORTRAN:* literal constants (integer `25`, real `3.14` or `1.5E3`, double precision `1.0D0`, logical `.TRUE.`, character `'A'`) and **named constants** with `PARAMETER (PI = 3.14159)`, which must be declared before use and cannot be changed later.

| | C | FORTRAN |
|---|---|---|
| Variable declaration | `int count = 5;` `float radius, area;` | `INTEGER COUNT` `REAL RADIUS, AREA` |
| Constant | `const int MAXN = 100;` `#define PI 3.14159` | `PARAMETER (PI = 3.14159)` |
| Character | `char grade = 'A';` | `CHARACTER*1 GRADE` |

```c
#include <stdio.h>
#define PI 3.14159                      /* symbolic constant */

int main(void)
{
    const int MAXN = 100;               /* constant variable */
    int count = 5;                      /* integer variable, initialised */
    float radius = 2.5f, area;          /* two float variables */
    char grade = 'A';                   /* character variable */

    area = PI * radius * radius;
    printf("count = %d, MAXN = %d, grade = %c\n", count, MAXN, grade);
    printf("area = %.3f\n", area);
    return 0;
}
```

```fortran
      PROGRAM VARS
      INTEGER COUNT
      REAL RADIUS, AREA
      CHARACTER*1 GRADE
      PARAMETER (PI = 3.14159)
      COUNT = 5
      RADIUS = 2.5
      GRADE = 'A'
      AREA = PI * RADIUS * RADIUS
      WRITE(*,*) COUNT, GRADE
      WRITE(*,*) AREA
      END
```

Output (C): `count = 5, MAXN = 100, grade = A` and `area = 19.635`. The FORTRAN program prints `5 A` and `19.63494`.

@s 3
**Syntax of the else-if ladder.**

```c
if (condition1)
    statement1;
else if (condition2)
    statement2;
else if (condition3)
    statement3;
...
else
    default_statement;
```

The conditions are tested from the top; the statement of the first true condition is executed and the rest of the ladder is skipped; the final `else` runs if no condition is true. Example (division from marks):

```c
#include <stdio.h>

int main(void)
{
    int marks;

    printf("Enter marks: ");
    scanf("%d", &marks);
    if (marks >= 80)
        printf("Distinction\n");
    else if (marks >= 60)
        printf("First division\n");
    else if (marks >= 45)
        printf("Second division\n");
    else if (marks >= 32)
        printf("Pass\n");
    else
        printf("Fail\n");
    return 0;
}
```

Input `72` gives `First division`.

**Syntax of do-while.**

```c
do {
    statements;
} while (condition);        /* semicolon is compulsory */
```

The body is executed first and the condition is tested afterwards, so the body runs at least once.

**Pattern program.** Row $i$ ($i=1,\dots,4$) has $i$ numbers, the multiples $i, 2i, \dots, i\cdot i$, preceded by $4-i$ blank columns, which gives the right-aligned triangle $1;\ 2\ 4;\ 3\ 6\ 9;\ 4\ 8\ 12\ 16$. The inner loop uses `do-while`:

```c
#include <stdio.h>

int main(void)
{
    int i, j, rows = 4;

    for (i = 1; i <= rows; i++) {
        for (j = 1; j <= rows - i; j++)     /* leading blanks */
            printf("   ");
        j = 1;
        do {
            printf("%-3d  ", i * j);        /* i-th multiples: i, 2i, ..., i*i */
            j++;
        } while (j <= i);
        printf("\n");
    }
    return 0;
}
```

Output:

```text
         1
      2    4
   3    6    9
4    8    12   16
```

@s 4
**Recursive power function.** $x^y = x\cdot x^{y-1}$ with $x^0 = 1$. The function calls itself with $y-1$ until the base case $y=0$ is reached, then the values are multiplied on the way back:

```c
#include <stdio.h>

long power(int x, int y)
{
    if (y == 0)
        return 1;                       /* base case: x^0 = 1 */
    return x * power(x, y - 1);         /* x^y = x * x^(y-1) */
}

int main(void)
{
    int x, y;

    printf("Enter x and y (y >= 0): ");
    scanf("%d %d", &x, &y);
    printf("%d^%d = %ld\n", x, y, power(x, y));
    return 0;
}
```

**How it works.** For $x=2$, $y=3$ the calls are

```text
power(2,3) = 2 * power(2,2)
                 power(2,2) = 2 * power(2,1)
                                  power(2,1) = 2 * power(2,0)
                                                   power(2,0) = 1      (base case)
                                  power(2,1) = 2 * 1 = 2
                 power(2,2) = 2 * 2 = 4
power(2,3) = 2 * 4 = 8
```

Each call is stored on the **stack** (with its own `x` and `y`); the recursion stops at the base case; without it the recursion would not end (stack overflow). Time: $y+1$ calls, i.e. $O(y)$. Outputs: `2^10 = 1024`, `3^4 = 81`. The return type is `long` so that larger powers fit. (Only non-negative $y$ is handled.)

@s 5
**`toupper()` and `tolower()`** (declared in `<ctype.h>`).

- `int toupper(int ch);` returns the **upper-case** equivalent of the letter `ch` (`toupper('a')` gives `'A'`); if `ch` is not a lower-case letter it is returned unchanged.
- `int tolower(int ch);` returns the **lower-case** equivalent of the letter `ch` (`tolower('Q')` gives `'q'`).

They are used to convert text, e.g. `str[i] = toupper(str[i]);`, and to make comparisons case-insensitive.

**Program.** The names are read into a 2-D character array, sorted with a bubble sort using a **case-insensitive comparison** built on `tolower()` (so `nepal`, `Bhutan` sort correctly), and displayed with the first letter changed to upper case with `toupper()`:

```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int cmpi(const char *a, const char *b)   /* case-insensitive comparison */
{
    while (*a && *b && tolower((unsigned char)*a) == tolower((unsigned char)*b)) {
        a++; b++;
    }
    return tolower((unsigned char)*a) - tolower((unsigned char)*b);
}

int main(void)
{
    char name[50][30], temp[30];
    int n, i, j;

    printf("How many countries? ");
    scanf("%d", &n);
    printf("Enter the names:\n");
    for (i = 0; i < n; i++)
        scanf("%s", name[i]);

    for (i = 0; i < n - 1; i++)
        for (j = 0; j < n - 1 - i; j++)
            if (cmpi(name[j], name[j + 1]) > 0) {
                strcpy(temp, name[j]);
                strcpy(name[j], name[j + 1]);
                strcpy(name[j + 1], temp);
            }

    printf("Countries in alphabetical order:\n");
    for (i = 0; i < n; i++) {
        name[i][0] = toupper((unsigned char)name[i][0]);   /* capitalise first letter */
        printf("%s\n", name[i]);
    }
    return 0;
}
```

Sample: for 5 names `nepal india Bhutan china japan` the output is `Bhutan`, `China`, `India`, `Japan`, `Nepal` (one per line).

@s 6
**Declaration of pointers.** A pointer is a variable that stores the **address** of another variable. It is declared with `*` and a data type that is the type of the variable it points to:
```c
data_type *pointer_name;        /* int *p;  float *q;  char *s; */
```
**Initialisation.** A pointer must be given a valid address before it is used: with the address-of operator `&`, with another pointer or the name of an array, or with `NULL`:
```c
int x = 25, *p = &x;      /* p holds the address of x */
float f = 3.5f, *q;
q = &f;                   /* assignment of an address */
int a[4], *r = a;         /* array name = address of a[0] */
int *z = NULL;            /* points nowhere */
```
The value of the variable is obtained by **dereferencing**: `*p` (so `*p = *p + 5` changes `x`).

**Pointer arithmetic.** The operations allowed on a pointer `p` that points into an array are:

1. `p + n`, `p - n`, `p++`, `p--`, `p += n`: move the pointer by $n$ elements, i.e. by $n\times$ `sizeof(type)` bytes (with 4-byte `int`, `p + 1` is 4 bytes higher; in a 16-bit compiler, 2 bytes);
2. `q - p`: the number of elements between two pointers of the same array;
3. comparisons `p < q`, `p == q`;
4. `*(a + i)` is the same as `a[i]`.

Addition of two pointers, multiplication and division by a number are **not allowed**.

```c
#include <stdio.h>

int main(void)
{
    int x = 25, *p;                     /* declaration */
    float f = 3.5f, *q = &f;            /* declaration with initialisation */
    int a[4] = {5, 10, 15, 20}, *r = a; /* pointer to the first element */

    p = &x;                             /* initialisation: address of x */
    printf("x = %d, *p = %d, p = address of x\n", x, *p);
    *p = *p + 5;                        /* change x through the pointer */
    printf("after *p = *p + 5: x = %d\n", x);
    printf("*q = %.1f\n", *q);

    printf("*r = %d\n", *r);
    r = r + 2;                          /* two ints ahead */
    printf("r + 2 -> *r = %d\n", *r);
    r--;
    printf("r-- -> *r = %d\n", *r);
    printf("&a[3] - r = %ld\n", (long)(&a[3] - r));
    return 0;
}
```

Output:

```text
x = 25, *p = 25, p = address of x
after *p = *p + 5: x = 30
*q = 3.5
*r = 5
r + 2 -> *r = 15
r-- -> *r = 10
&a[3] - r = 2
```

@s 7
**Design.** In a **16-bit compiler (Turbo C)** an `int` is 2 bytes (range $-32768$ to $32767$), so a **6-digit ID** (up to $999999$) and a **salary of 40,000** cannot be held in an `int`: they are declared `long` (4 bytes). 40,000 records of $4+30+4 = 38$ bytes each occupy about $1.5$ MB, which is far more than one 64 KB data segment of a 16-bit program, so an array of 40,000 structures is impossible. The records are therefore **stored in a binary file** (`karma.dat`) with `fwrite()` and `search()` reads them one at a time with `fread()` and compares the salary.

```c
#include <stdio.h>

struct karmachari {
    long id;                    /* 6-digit ID: needs long in a 16-bit compiler */
    char name[30];
    long salary;                /* 40000 does not fit in a 16-bit int */
};

void search(long sal)           /* scans the records stored in the file */
{
    FILE *fp = fopen("karma.dat", "rb");
    struct karmachari k;
    int found = 0;

    if (fp == NULL) { printf("File not found\n"); return; }
    while (fread(&k, sizeof(k), 1, fp) == 1)
        if (k.salary == sal) {
            printf("%06ld  %-20s %ld\n", k.id, k.name, k.salary);
            found = 1;
        }
    fclose(fp);
    if (!found)
        printf("No employee with salary %ld\n", sal);
}

int main(void)
{
    FILE *fp = fopen("karma.dat", "wb");
    struct karmachari k;
    long i, n, sal;

    if (fp == NULL) return 1;
    printf("Number of employees (up to 40000): ");
    scanf("%ld", &n);
    for (i = 0; i < n; i++) {
        printf("ID name salary: ");
        scanf("%ld %s %ld", &k.id, k.name, &k.salary);
        fwrite(&k, sizeof(k), 1, fp);
    }
    fclose(fp);

    printf("Salary to search: ");
    scanf("%ld", &sal);
    search(sal);
    return 0;
}
```

Test run (3 records): `100234 Ram 40000`, `100235 Sita 52000`, `100236 Hari 40000`; searching for `40000` prints

```text
100234  Ram                  40000
100236  Hari                 40000
```

and a salary that is not present prints `No employee with salary ...`. (For a modern 32-bit compiler an array `struct karmachari k[40000];` can also be used.) `%06ld` prints the ID with leading zeros up to 6 digits.

@s 8
**Method.** (1) Open `Source` for writing and write each prime of the range into it (a number is prime if no integer from 2 to $\sqrt n$ divides it); (2) reopen `Source` for reading, `Destination` for writing, and copy it character by character; (3) reopen `Destination` for reading and display it.

```c
#include <stdio.h>

int isPrime(int n)
{
    int i;
    if (n < 2) return 0;
    for (i = 2; i * i <= n; i++)
        if (n % i == 0) return 0;
    return 1;
}

int main(void)
{
    FILE *src, *dst;
    int n1, n2, n, ch;

    printf("Enter n1 and n2: ");
    scanf("%d %d", &n1, &n2);

    src = fopen("Source", "w");                 /* 1. primes -> Source */
    if (src == NULL) { printf("Cannot create Source\n"); return 1; }
    for (n = n1; n <= n2; n++)
        if (isPrime(n))
            fprintf(src, "%d\n", n);
    fclose(src);

    src = fopen("Source", "r");                 /* 2. copy Source -> Destination */
    dst = fopen("Destination", "w");
    if (src == NULL || dst == NULL) { printf("Cannot open files\n"); return 1; }
    while ((ch = fgetc(src)) != EOF)
        fputc(ch, dst);
    fclose(src);
    fclose(dst);

    dst = fopen("Destination", "r");            /* 3. display Destination */
    printf("Content of Destination:\n");
    while ((ch = fgetc(dst)) != EOF)
        putchar(ch);
    fclose(dst);
    return 0;
}
```

For `n1 = 10`, `n2 = 40` both files contain the primes `11 13 17 19 23 29 31 37` (one per line) and the program displays

```text
Content of Destination:
11
13
17
19
23
29
31
37
```

@s 9
The Fibonacci sequence $0,1,1,2,3,5,8,13,\dots$ starts with $a = 0$, $b = 1$, and each new term is the sum of the previous two. A `DO` loop prints $n$ terms:

```fortran
      PROGRAM FIBO
      INTEGER N, I, A, B, C
      WRITE(*,*) 'ENTER N'
      READ(*,*) N
      A = 0
      B = 1
      WRITE(*,*) 'FIBONACCI SEQUENCE:'
      DO 10 I = 1, N
         WRITE(*,*) A
         C = A + B
         A = B
         B = C
   10 CONTINUE
      END
```

Compiled with gfortran and run for $n=10$: `0 1 1 2 3 5 8 13 21 34`. Each pass of the loop prints `A`, then computes `C = A + B`, shifts `A = B` and `B = C`. (For $n = 1$ only `0` is printed.)

@s 10
**Switch statement vs user-defined function.**

| `switch` statement | User-defined function |
|---|---|
| A **decision (selection) statement**: chooses one of several blocks of code according to the value of an integer/character expression | A **named, reusable block of code** that performs one task and may return a value |
| Syntax: `switch (expr) { case 1: ... break; default: ... }` | Syntax: `type name(parameters) { body; return value; }` |
| Part of the same function; control goes to the matching `case` and falls through unless `break` is used | Called from other functions; control returns to the caller; it may be recursive |
| Tests only equality with integer/char constants (no ranges, no floats) | Can take any arguments and do any computation |
| Does not give modularity or reuse | Gives **modularity**, reuse, easier testing and debugging, smaller programs |

A function is often called from a `case` of a `switch` (menu-driven programs).

**Transpose of an $N\times N$ matrix.** The transpose $A^T$ has the elements $t_{ji} = a_{ij}$ (rows become columns). A user-defined function does the work:

```c
#include <stdio.h>

void transpose(int a[10][10], int t[10][10], int n)
{
    int i, j;
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            t[j][i] = a[i][j];
}

void show(int m[10][10], int n)
{
    int i, j;
    for (i = 0; i < n; i++) {
        for (j = 0; j < n; j++)
            printf("%4d", m[i][j]);
        printf("\n");
    }
}

int main(void)
{
    int a[10][10], t[10][10], n, i, j;

    printf("Order N of the square matrix: ");
    scanf("%d", &n);
    printf("Enter %d elements:\n", n * n);
    for (i = 0; i < n; i++)
        for (j = 0; j < n; j++)
            scanf("%d", &a[i][j]);
    transpose(a, t, n);
    printf("Original matrix:\n");
    show(a, n);
    printf("Transpose:\n");
    show(t, n);
    return 0;
}
```

Test, $N = 3$ with input `1 2 3 4 5 6 7 8 9`:

```text
Original matrix:
   1   2   3
   4   5   6
   7   8   9
Transpose:
   1   4   7
   2   5   8
   3   6   9
```
