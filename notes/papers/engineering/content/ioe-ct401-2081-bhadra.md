---
file: NEBians-IOE-Past-Paper-Computer-Programming-CT401-2081-Bhadra.pdf
subject: Computer Programming
level: BE · Year I / Part I
code: CT 401
year_bs: 2081 Bhadra
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
Differentiate between system software and application software. What are the basic steps needed to be followed for developing a software? Explain. [[2+4]]

@q 2
Define operator and keyword in C. Write an algorithm and draw the flowchart to calculate the factorial of a positive integer. [[2+6]]

@q 3
Write syntax and example of the following. [[6]]

- i) `getch()`
- ii) `gets()`
- iii) `printf()`
- iv) `scanf()`

@q 4
Differentiate between do loop and while loop in C. Write a program to check whether a given N-digit positive number is Armstrong or not. [Hint: a number that is equal to the sum of its own digits each raised to the power. E.g. $1634 = 1^4+6^4+3^4+4^4 = 1634$] [[3+5]]

@q 5
Explain how array can be passed to the function. Write a program to read and sort the N elements of a 1-D array in ascending order and display the sorted elements. [[2+5]]

@q 6
Write a program to find the length of a string without using string handling function. [[3]]

@q 7
Explain function prototyping. Write a program to find the Fibonacci series up to $n$ terms using the concept of recursive function. [[2+5]]

@q 8
What do you mean by nested structure? Explain. Write a program to demonstrate the use of `.` and `->` operator in structure. [[3+5]]

@q 9
Write a program to illustrate the concept of pointer arithmetic. [[4]]

@q 10
Differentiate between text file and binary file. Write a program to read positive integers from users and write all the odd integers to ODD.txt and all even integers to the EVEN.txt. [[3+3]]

@q 11
Explain how Arithmetic IF statement works in FORTRAN. Write a program in FORTRAN to check whether a given $n$-digit positive number is a palindrome or not. [hint: a palindrome number is a number that remains same when its digits are reversed] [[3+6]]

@q 12
Write short notes on: [[2×4]]

i) Call by value vs call by reference method in functions

ii) `break` vs `continue` in loop termination
<!-- SOLUTIONS -->
@s 1
**System software vs application software.**

| System software | Application software |
|---|---|
| Manages and controls the computer hardware and provides a platform to run other software | Performs a specific task for the user (document, calculation, game, accounting) |
| Runs in the background, starts when the computer is switched on and runs until it is off | Runs only when the user starts it |
| General purpose, written in low-level languages (C, assembly) | Written in high-level languages (Java, C++, Python, VB) |
| Hardware dependent; essential for the computer to work | Not essential for the computer to work; runs on top of the system software |
| Examples: operating system (Windows, Linux), device drivers, compilers, assemblers, utility programs | Examples: MS Word, Excel, web browser, media player, payroll system |

**Basic steps of software development (software development life cycle, SDLC).**

```figure caption="Question 1: the basic steps of software development (waterfall model); testing and maintenance feed errors and change requests back to the earlier stages."
fig,ax=plt.subplots(figsize=(6.4,3.0)); ax.axis('off'); ax.set_xlim(0,14); ax.set_ylim(-0.6,7)
names=['1 Problem\ndefinition','2 Analysis','3 Design','4 Coding','5 Testing and\ndebugging','6 Implement,\nmaintain']
for i,t in enumerate(names):
    x=0.1+i*2.25; y=6.0-i*0.95
    ax.add_patch(plt.Rectangle((x,y-0.4),2.1,0.8,fc='#e8eef7',ec='#1d6fb8',lw=1.2)); ax.text(x+1.05,y,t,ha='center',va='center',fontsize=7)
    if i<5: ax.annotate('',xy=(x+2.25+0.3,y-0.95+0.4),xytext=(x+1.8,y-0.4),arrowprops=dict(arrowstyle='->',color='#14181f'))
ax.annotate('',xy=(1.0,5.5),xytext=(12.2,0.75),arrowprops=dict(arrowstyle='->',color='#d9534f',ls='--',connectionstyle='arc3,rad=0.25'))
ax.text(5.0,-0.3,'feedback: errors found, changes requested',color='#d9534f',fontsize=8,ha='center')
```

1. **Problem definition and feasibility study:** state clearly what the software must do, its users, inputs, outputs and constraints (time, cost, technology).
2. **Requirement analysis:** collect and analyse the user requirements, and write them down as the *software requirement specification* (SRS).
3. **Design:** plan the solution: the overall architecture and modules, data structures, algorithms and flowcharts, the user interface and database design.
4. **Coding (implementation):** translate the design into a program in a suitable programming language; modules are written and compiled, following the coding standard.
5. **Testing and debugging:** run the program with test data (unit, integration, system, acceptance tests) to find errors; locate and correct them (debugging) and test again.
6. **Implementation (deployment), documentation and maintenance:** install the system at the user's site, train users, prepare the user manual and technical documentation, and then correct faults, adapt and enhance the software over its life.

@s 2
**Operator.** A symbol that tells the compiler to perform a specific **mathematical, relational or logical operation** on one or more operands, e.g. `+ - * / %` (arithmetic), `< > == !=` (relational), `&& || !` (logical), `=` (assignment), `++ --`, `sizeof`, `&`, `*`. Example: in `c = a + b;`, `+` and `=` are operators and `a`, `b`, `c` are operands.

**Keyword.** A **reserved word** of the C language that has a fixed, predefined meaning for the compiler; it cannot be used as a variable or function name. There are 32 keywords in ANSI C: `int, float, char, double, if, else, for, while, do, switch, case, break, continue, return, void, struct, union, enum, typedef, static, sizeof`, etc. Example: `int` in `int x;` declares an integer variable.

**Algorithm for the factorial of a positive integer** ($n! = 1\times2\times3\times\cdots\times n$, $0! = 1$):

1. Start.
2. Read $n$.
3. Set fact $= 1$ and $i = 1$.
4. While $i\le n$ repeat: fact $=$ fact $\times\ i$ and $i = i+1$.
5. Print fact.
6. Stop.

```figure caption="Question 2: flowchart for the factorial of a positive integer."
fig, ax = plt.subplots(figsize=(4.6, 4.4))
def B(x, y, t, k='p', w=2.2, h=0.7):
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
B(0,8.7,'Start','t'); A(0,8.35,0,8.0)
B(0,7.6,'Read n','io'); A(0,7.25,0,6.9)
B(0,6.5,'fact = 1, i = 1'); A(0,6.15,0,5.75)
B(0,5.0,'i <= n ?','d',w=2.2); A(0.7,5.0,1.9,5.0,'Yes'); A(0,4.4,0,3.7,'No')
B(3.1,5.0,'fact = fact * i\ni = i + 1',w=2.2,h=0.8)
L([3.1,3.1],[5.4,5.75]); L([3.1,0],[5.75,5.75])
B(0,3.3,'Print fact','io'); A(0,2.95,0,2.3)
B(0,1.95,'Stop','t')
ax.set_xlim(-2, 6.4); ax.set_ylim(1.6, 9.1); ax.axis('off')
```

For $n = 5$: fact $= 1\cdot1\cdot2\cdot3\cdot4\cdot5 = 120$. The corresponding C program (tested):

```c
#include <stdio.h>

int main(void)
{
    int n, i;
    unsigned long long fact = 1;

    printf("Enter a positive integer: ");
    scanf("%d", &n);
    if (n < 0) {
        printf("Factorial is not defined for a negative number\n");
        return 0;
    }
    for (i = 1; i <= n; i++)
        fact = fact * i;
    printf("Factorial of %d = %llu\n", n, fact);
    return 0;
}
```

Sample runs: `5` gives `Factorial of 5 = 120`; `20` gives `Factorial of 20 = 2432902008176640000` (the largest factorial that fits in `unsigned long long` is $20!$).

@s 3
| Function | Header | Syntax | Meaning |
|---|---|---|---|
| **i) `getch()`** | `<conio.h>` | `int getch(void);`  `ch = getch();` | Reads **one character from the keyboard without echoing** it on the screen and without waiting for Enter. Used to hold the screen or to read a password. |
| **ii) `gets()`** | `<stdio.h>` | `char *gets(char *str);`  `gets(str);` | Reads a **whole line (including blanks)** from the keyboard into the string `str` until Enter; the newline is replaced by `'\0'`. (Unsafe, no limit check; `fgets()` is preferred.) |
| **iii) `printf()`** | `<stdio.h>` | `printf("format string", arg1, arg2, ...);` | Writes **formatted output** to the screen using conversion specifiers `%d %f %c %s %ld`, etc. Returns the number of characters printed. |
| **iv) `scanf()`** | `<stdio.h>` | `scanf("format string", &arg1, &arg2, ...);` | Reads **formatted input** from the keyboard and stores it at the **addresses** of the variables (`&`). Returns the number of items read successfully. |

Examples:

```c
#include <stdio.h>
#include <conio.h>

int main(void)
{
    char ch, name[40];
    int age;
    float cgpa;

    printf("Enter age and CGPA: ");              /* printf */
    scanf("%d %f", &age, &cgpa);                 /* scanf  */
    getchar();                                   /* absorb the Enter key */
    printf("Enter your full name: ");
    gets(name);                                  /* gets: reads blanks too */
    printf("Name = %s, age = %d, CGPA = %.2f\n", name, age, cgpa);
    printf("Press any key to continue...");
    ch = getch();                                /* getch: no echo, no Enter */
    return 0;
}
```

Sample: input `20 3.75` and `Ram Bahadur` prints `Name = Ram Bahadur, age = 20, CGPA = 3.75`. (`getch()` is a non-standard function of `<conio.h>`, available in Turbo C.)

@s 4
**Difference between `do` loop and `while` loop.**

| `while` loop (entry-controlled) | `do ... while` loop (exit-controlled) |
|---|---|
| The condition is **tested first**, then the body is executed | The body is executed **first**, then the condition is tested |
| If the condition is false at the start, the body is executed **zero times** | The body is executed **at least once** even if the condition is false |
| No semicolon after the condition | A **semicolon** is needed after `while (condition);` |
| Syntax: `while (cond) { body }` | Syntax: `do { body } while (cond);` |
| Used when the number of iterations may be zero | Used for menus and input validation where one pass is always needed |

**Armstrong number program.** An $N$-digit number is Armstrong if the sum of the $N$-th powers of its digits equals the number. First count the digits $N$, then sum $d^N$ for each digit:

```c
#include <stdio.h>

int main(void)
{
    long n, temp, sum = 0;
    int digits = 0, d, i;

    printf("Enter a positive integer: ");
    scanf("%ld", &n);

    temp = n;
    while (temp > 0) {              /* count the digits */
        digits++;
        temp /= 10;
    }

    temp = n;
    while (temp > 0) {              /* sum of digit^digits */
        long p = 1;
        d = temp % 10;
        for (i = 0; i < digits; i++)
            p *= d;
        sum += p;
        temp /= 10;
    }

    if (sum == n)
        printf("%ld is an Armstrong number\n", n);
    else
        printf("%ld is not an Armstrong number\n", n);
    return 0;
}
```

Check for $1634$: $N = 4$, $1^4+6^4+3^4+4^4 = 1+1296+81+256 = 1634$. Outputs: `1634 is an Armstrong number`, `153 is an Armstrong number` ($1^3+5^3+3^3 = 153$), `9474 is an Armstrong number`, `123 is not an Armstrong number` ($1+8+27 = 36$).

@s 5
**Passing an array to a function.** The **name of an array is the address of its first element**, so when an array is passed to a function only this base address is passed (**call by reference**). The array is *not* copied: the function works on the original array, and any change made inside the function is visible in the caller. The size is passed as a separate argument.

- Function definition: `void sortArray(int a[], int n)` or equivalently `void sortArray(int *a, int n)`
- Function call: `sortArray(a, n);` (no `[]` and no `&` with the array name)
- A single element can also be passed by value: `f(a[2])`.

**Program** (read $N$ elements, sort ascending by bubble sort, display):

```c
#include <stdio.h>

void readArray(int a[], int n)
{
    int i;
    for (i = 0; i < n; i++) {
        printf("a[%d] = ", i);
        scanf("%d", &a[i]);
    }
}

void sortArray(int a[], int n)          /* bubble sort, ascending */
{
    int i, j, t;
    for (i = 0; i < n - 1; i++)
        for (j = 0; j < n - 1 - i; j++)
            if (a[j] > a[j + 1]) {
                t = a[j]; a[j] = a[j + 1]; a[j + 1] = t;
            }
}

void display(int a[], int n)
{
    int i;
    for (i = 0; i < n; i++)
        printf("%d ", a[i]);
    printf("\n");
}

int main(void)
{
    int a[100], n;

    printf("How many elements? ");
    scanf("%d", &n);
    readArray(a, n);                    /* array name = address of a[0] */
    sortArray(a, n);
    printf("Sorted elements: ");
    display(a, n);
    return 0;
}
```

Sample: for $n = 6$ and the input `42 7 19 3 88 1` the output is `Sorted elements: 1 3 7 19 42 88`.

@s 6
**Length of a string without library functions.** A C string ends with the null character `'\0'`, so count the characters until it is reached:

```c
#include <stdio.h>

int main(void)
{
    char str[100];
    int i = 0;

    printf("Enter a string: ");
    scanf("%99[^\n]", str);
    while (str[i] != '\0')
        i++;
    printf("Length of the string = %d\n", i);
    return 0;
}
```

Sample: input `Programming is fun` gives `Length of the string = 18` (blanks are counted, the null is not). `scanf("%99[^\n]", str)` reads a whole line including blanks and is safe for a 100-byte array.

@s 7
**Function prototyping.** A **function prototype** is the declaration of a function placed *before its first call* (usually at the top of the program or in a header file) that tells the compiler the function's **name, return type, number and types of its parameters**:
```c
return_type function_name(type1 arg1, type2 arg2, ...);
int fib(int n);                 /* the parameter name may be omitted: int fib(int); */
```
Uses: (i) the compiler can **check the number and type of arguments and the return value** at each call and convert the types automatically, (ii) a function may be **defined after `main()`**, which makes the program easier to read, and (iii) it avoids the old implicit `int` assumption. The prototype is followed by a semicolon; the definition has the body.

**Fibonacci series using recursion.** The series is $0,1,1,2,3,5,8,\dots$ with $F_0 = 0$, $F_1 = 1$, $F_n = F_{n-1}+F_{n-2}$. A function that calls itself with $n-1$ and $n-2$, with the base cases $F_0$ and $F_1$, gives the $n$-th term, and a loop in `main()` prints the first $n$ terms:

```c
#include <stdio.h>

int fib(int n);                         /* function prototype */

int main(void)
{
    int n, i;

    printf("Enter number of terms: ");
    scanf("%d", &n);
    printf("Fibonacci series: ");
    for (i = 0; i < n; i++)
        printf("%d ", fib(i));
    printf("\n");
    return 0;
}

int fib(int n)                          /* recursive definition */
{
    if (n == 0) return 0;
    if (n == 1) return 1;
    return fib(n - 1) + fib(n - 2);
}
```

For $n = 8$ the output is `Fibonacci series: 0 1 1 2 3 5 8 13`.

@s 8
**Nested structure.** A structure that has **another structure as one of its members** is called a nested structure. It is used to group related data hierarchically; the inner structure must be defined (or declared) before the outer one. Example: an employee has a date of birth, which is itself made up of day, month and year:

```c
struct Date { int day, month, year; };

struct Employee {
    char name[30];
    int id;
    struct Date dob;        /* nested structure */
    float salary;
};
```

A member of the inner structure is reached with **two dot operators**: `e.dob.year`. A structure can also be nested by defining the inner structure inside the outer one.

**The `.` and `->` operators.**

- The **dot (member) operator** `.` is used with a **structure variable**: `e.id`.
- The **arrow (indirect member) operator** `->` is used with a **pointer to a structure**: `p->id`, which is the same as `(*p).id`.

**Program:**

```c
#include <stdio.h>

struct Date {
    int day, month, year;
};

struct Employee {
    char name[30];
    int id;
    struct Date dob;                    /* nested structure */
    float salary;
};

int main(void)
{
    struct Employee e = {"Sita Sharma", 101, {15, 6, 2000}, 45000.0f};
    struct Employee *p = &e;

    /* dot operator: through the structure variable */
    printf("Using . operator\n");
    printf("Name   : %s\n", e.name);
    printf("ID     : %d\n", e.id);
    printf("DOB    : %d/%d/%d\n", e.dob.day, e.dob.month, e.dob.year);
    printf("Salary : %.2f\n", e.salary);

    /* arrow operator: through a pointer to the structure */
    printf("\nUsing -> operator\n");
    printf("Name   : %s\n", p->name);
    printf("ID     : %d\n", p->id);
    printf("DOB    : %d/%d/%d\n", p->dob.day, p->dob.month, p->dob.year);
    p->salary += 5000;                  /* modify through the pointer */
    printf("Raised salary : %.2f\n", e.salary);
    return 0;
}
```

Output:

```text
Using . operator
Name   : Sita Sharma
ID     : 101
DOB    : 15/6/2000
Salary : 45000.00

Using -> operator
Name   : Sita Sharma
ID     : 101
DOB    : 15/6/2000
Raised salary : 50000.00
```

@s 9
**Pointer arithmetic.** Only the following arithmetic is allowed on pointers: adding or subtracting an integer (`p + n`, `p - n`, `p++`, `p--`), and subtracting two pointers of the same array (`q - p`) which gives the number of elements between them. A pointer is moved in units of the **size of the type it points to**: if `p` is an `int *` and an `int` is $4$ bytes, `p + 1` is the address $4$ bytes higher, i.e. the next element. Addition of two pointers, multiplication and division are not allowed. The array element `a[i]` is the same as `*(a + i)`.

```c
#include <stdio.h>

int main(void)
{
    int a[5] = {10, 20, 30, 40, 50};
    int *p = a, *q;
    int i;

    printf("p points to a[0]: *p = %d\n", *p);
    p = p + 2;                          /* moves 2 elements = 2*sizeof(int) bytes */
    printf("after p = p + 2 : *p = %d\n", *p);
    p++;
    printf("after p++       : *p = %d\n", *p);
    p--;
    printf("after p--       : *p = %d\n", *p);
    q = &a[4];
    printf("q - p = %ld elements\n", (long)(q - p));
    printf("*(a + 4) = %d, *(p - 2) = %d\n", *(a + 4), *(p - 2));
    printf("All elements through the pointer: ");
    for (p = a, i = 0; i < 5; i++)
        printf("%d ", *(p + i));
    printf("\n");
    return 0;
}
```

Output:

```text
p points to a[0]: *p = 10
after p = p + 2 : *p = 30
after p++       : *p = 40
after p--       : *p = 30
q - p = 2 elements
*(a + 4) = 50, *(p - 2) = 10
All elements through the pointer: 10 20 30 40 50
```

@s 10
**Text file vs binary file.**

| Text file | Binary file |
|---|---|
| Stores data as **ASCII characters**, human readable | Stores data in the **same form as in memory (raw bytes)**, not readable in an editor |
| Opened with modes `"r"`, `"w"`, `"a"` | Opened with modes `"rb"`, `"wb"`, `"ab"` |
| Newline translated (`\n` becomes `\r\n` on Windows); an end-of-file marker is used | No translation of characters, the file ends at the byte count |
| Accessed with `fprintf()`, `fscanf()`, `fgets()`, `fputs()`, `fgetc()`, `fputc()` | Accessed with `fread()`, `fwrite()` |
| Larger size, slower, because numbers are converted to characters | Compact and faster; random access with `fseek()` is simple |
| Example: `.txt`, `.c` | Example: `.exe`, `.jpg`, `.dat` |

**Program** (reads integers until 0 or a negative number is entered; odd ones go to `ODD.txt`, even ones to `EVEN.txt`):

```c
#include <stdio.h>

int main(void)
{
    FILE *fodd, *feven;
    int n;

    fodd  = fopen("ODD.txt",  "w");
    feven = fopen("EVEN.txt", "w");
    if (fodd == NULL || feven == NULL) {
        printf("Cannot open the files\n");
        return 1;
    }
    printf("Enter positive integers (0 or a negative number to stop):\n");
    while (scanf("%d", &n) == 1 && n > 0) {
        if (n % 2 == 0)
            fprintf(feven, "%d\n", n);
        else
            fprintf(fodd, "%d\n", n);
    }
    fclose(fodd);
    fclose(feven);
    printf("Odd numbers are in ODD.txt, even numbers in EVEN.txt\n");
    return 0;
}
```

For the input `12 7 30 5 18 9 0`, `ODD.txt` contains `7`, `5`, `9` and `EVEN.txt` contains `12`, `30`, `18` (one per line).

@s 11
**Arithmetic IF statement in FORTRAN.** The **arithmetic IF** is a three-way branch on the sign of an arithmetic expression:
```fortran
IF (expression) label1, label2, label3
```
The expression (integer or real) is evaluated and control passes to

- `label1` if the value is **negative** ($<0$),
- `label2` if the value is **zero** ($=0$),
- `label3` if the value is **positive** ($>0$).

For example `IF (X - 5) 10, 20, 30` goes to statement 10 if $X<5$, to 20 if $X=5$, to 30 if $X>5$. It is usually combined with `GO TO` and the labelled statements. (It is an older FORTRAN feature, kept for compatibility.)

**Palindrome program.** The digits of $N$ are reversed with `MOD` and integer division, building $R = 10R + d$, and then $R$ is compared with $N$ (the difference being zero means a palindrome):

```fortran
      PROGRAM PALIN
      INTEGER N, M, R, D
      PRINT *, 'ENTER A POSITIVE INTEGER'
      READ *, N
      M = N
      R = 0
   10 IF (M) 99, 30, 20
   20 D = MOD(M, 10)
      R = R * 10 + D
      M = M / 10
      GO TO 10
   30 IF (R - N) 40, 50, 40
   40 PRINT *, N, ' IS NOT A PALINDROME'
      GO TO 60
   50 PRINT *, N, ' IS A PALINDROME'
   60 STOP
   99 PRINT *, 'NUMBER MUST BE POSITIVE'
      END
```

Flow of the program: statement 10 tests `M` (negative gives 99, zero gives 30 meaning all digits are used, positive gives 20 to take one more digit); statement 30 tests `R - N` (non-zero gives 40, zero gives 50).

Sample runs (compiled with gfortran and run): `12321` gives `IS A PALINDROME`; `1234` gives `IS NOT A PALINDROME`; `1001` and `7` are palindromes.

Trace for $N = 12321$: $R = 1, 12, 123, 1232, 12321$ and $R - N = 0$, so it is a palindrome. For $N = 1234$: $R = 4321\ne1234$.

@s 12
**i) Call by value vs call by reference.**

| Call by value | Call by reference (address) |
|---|---|
| The **values** of the actual arguments are **copied** into the formal parameters | The **addresses** of the actual arguments are passed to **pointer** parameters |
| Changes made in the function do **not** affect the actual arguments | Changes made through the pointers **do** change the caller's variables |
| Needs extra memory for the copies, which is not an issue for small data | No copy of the data, efficient for large data (arrays, structures) |
| Call: `swap(a, b);` Definition: `void swap(int x, int y)` | Call: `swap(&a, &b);` Definition: `void swap(int *x, int *y)` |
| Only one value can be returned, using `return` | Several values can be returned/modified |

```c
#include <stdio.h>

void swapVal(int x, int y)   { int t = x; x = y; y = t; }
void swapRef(int *x, int *y) { int t = *x; *x = *y; *y = t; }

int main(void)
{
    int a = 5, b = 9;
    swapVal(a, b);
    printf("after swapVal: a = %d, b = %d\n", a, b);   /* 5, 9: unchanged */
    swapRef(&a, &b);
    printf("after swapRef: a = %d, b = %d\n", a, b);   /* 9, 5: swapped */
    return 0;
}
```

**ii) `break` vs `continue`.**

| `break` | `continue` |
|---|---|
| **Terminates the loop** (or `switch`) completely; control goes to the first statement after the loop | **Skips the rest of the current iteration** and goes to the next iteration (to the condition test, or to the increment in a `for` loop) |
| Can be used in loops and in `switch` | Can be used **only in loops** |
| Example: stop searching when the item is found | Example: skip the processing of unwanted values |

```c
for (i = 1; i <= 10; i++) {
    if (i == 4) continue;      /* skips 4 */
    if (i == 8) break;         /* leaves the loop at 8 */
    printf("%d ", i);
}                              /* prints: 1 2 3 5 6 7 */
```
