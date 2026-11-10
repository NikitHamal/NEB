---
file: NEBians-IOE-Past-Paper-Computer-Programming-CT401-2080-Bhadra.pdf
subject: Computer Programming
level: BE · Year I / Part I
code: CT 401
year_bs: 2080 Bhadra
cal: BS
year_ad: 2023
stream: All programmes except B.Arch and BAS
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Regular paper (old course, CT 401). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
Write about generation of Computer Programming with example. Draw a flowchart to calculate the area of triangle, where the values of three sides are read from the user. [Hint: $\text{Area} = \sqrt{s(s-a)(s-b)(s-c)}$ and $s = (a+b+c)/2$] [[4+4]]

@q 2
a) What are the fundamental data types in C? Explain about precedence and associativity of an operator with examples. [[2+2]]

b) Write down the output of following segment of a C program [[4]]

```c
void main()
{
    int n=90;
    printf("%10d \n",n);
    printf("%-2d \n",n);
    printf("%c \n",'A');
    printf("%-10d \n",n);
    getch();
}
```

@q 3
Compare else-if ladder with switch statement. Write a program to check whether the entered number is palindrome or not. [Hint: Palindrome number for example is 12321, this number is same when reversed] [[4+4]]

@q 4
Write the syntax of function prototypes for passing 1D and 2D array into user defined function in C. Write a program in C to read the elements of 2D array of any dimension. Add all the columns of that array using user defined function. Store the result in 1D array and display the same. [[2+6]]

@q 5
Write a C program (16-bit compiler) to read name, roll-number (must be a six-digit number) and marks obtained in five subjects of N students using structure. Where, N is the input provided by the user. Display the details of all students as well as the total marks and percentage obtained by each student. [[8]]

@q 6
a) Compare call by value and call by reference with example. [[4]]

b) Write the output of the program shown below [[4]]

```c
#include <stdio.h>
int main ()
{
    int a = 10, *ptr1, **ptr2;
    ptr1 = &a;
    ptr2 = &ptr1;
    printf ("%d\t %d \n", a,&a);
    printf ("%d\t %d \n",&ptr1, ptr1);
    printf ("%d\t %d \n", *ptr1, *ptr2);
    **ptr2 =20;
    printf ("%d", a);
    return 0;
}
```

| Variable | Value | Address |
|---|---|---|
| a | | 6422296 |
| ptr1 | | 6422292 |
| ptr2 | | 6422280 |

@q 7
Write the concept of string handling functions. Write a program in C to concatenate two strings without using string handling functions. [[2+6]]

@q 8
Write a program in C to create a structure book using its members: Name, Price and Author. Read one record from the user "book.txt". Read back the information from "book.txt" and display it. [[8]]

@q 9
Compare about the control structure available in C and FORTRAN. [[4+4]]

@q 10
Write a program in FORTRAN to sort an array of 100 numbers in ascending order. [[8]]
<!-- SOLUTIONS -->
@s 1
**Generations of programming languages.** Programming languages have developed through five generations, each one closer to the human language and further from the machine:

| Generation | Language type | Features | Example |
|---|---|---|---|
| **1GL** (1940s) | **Machine language** | Binary $0/1$ instructions, executed directly by the CPU, no translator needed; fast but very hard to write, machine dependent | `10110000 01100001` (8086: move 61H into AL) |
| **2GL** (1950s) | **Assembly language** | Mnemonics (`MOV`, `ADD`), translated by an **assembler**; still machine dependent | `MOV AL, 61H` |
| **3GL** (1960s-) | **High-level languages** | English-like, machine independent, translated by a **compiler or interpreter**; procedural | FORTRAN, COBOL, C, Pascal, BASIC; `c = a + b;` |
| **4GL** (1970s-) | **Very high-level, non-procedural** | State *what* is wanted, not how; database queries, report generators, code generators | SQL: `SELECT name FROM student WHERE marks > 80;` |
| **5GL** (1980s-) | **Artificial-intelligence / constraint languages** | The problem is described by constraints, and the system solves it; used in AI | Prolog, Mercury, OPS5 |

**Flowchart for the area of a triangle** (sides $a,b,c$; $s=(a+b+c)/2$; area $=\sqrt{s(s-a)(s-b)(s-c)}$):

```figure caption="Question 1: flowchart for the area of a triangle from the three sides."
fig, ax = plt.subplots(figsize=(4.4, 4.6))
def B(x, y, t, k='p', w=3.0, h=0.7):
    if k == 'd':
        ax.add_patch(plt.Polygon([[x, y+h*0.8], [x+w*0.5, y], [x, y-h*0.8], [x-w*0.5, y]], fc='#fff3e0', ec='#b8860b'))
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
B(0,9.3,'Start','t',w=2.0); A(0,8.95,0,8.6)
B(0,8.2,'Read a, b, c','io'); A(0,7.85,0,7.4)
B(0,6.8,'valid triangle?\n(a+b>c, b+c>a, a+c>b)','d',w=4.4,h=0.8); A(0,6.2,0,5.7,'Yes'); A(2.2,6.8,3.3,6.8,'No')
B(4.6,6.8,'Print\n"not a triangle"','io',w=2.2,h=0.8)
B(0,5.3,'s = (a + b + c) / 2'); A(0,4.95,0,4.5)
B(0,4.1,'area = sqrt(s(s-a)(s-b)(s-c))',w=3.8); A(0,3.75,0,3.3)
B(0,2.9,'Print area','io',w=2.2); A(0,2.55,0,2.1)
B(0,1.75,'Stop','t',w=2.0)
ax.plot([4.6,4.6],[6.4,1.75],color='#14181f',lw=1); ax.annotate('',xy=(1.0,1.75),xytext=(4.6,1.75),arrowprops=dict(arrowstyle='->',lw=1))
ax.set_xlim(-2.6, 6.2); ax.set_ylim(1.3, 9.7); ax.axis('off')
```

Check: sides $3,4,5$: $s=6$, area $=\sqrt{6\cdot3\cdot2\cdot1} = 6$. Program:

{{tri.c}}

Sample: `3 4 5` gives `Area of the triangle = 6.000`; `7 8 9` gives `26.833`.

@s 2
**a) Fundamental (basic) data types in C.**

| Type | Meaning | Size (typical 32-bit; 16-bit compiler) | Format |
|---|---|---|---|
| `char` | single character | 1 byte | `%c` |
| `int` | integer | 4 bytes; 2 bytes in a 16-bit compiler | `%d` |
| `float` | single-precision real | 4 bytes | `%f` |
| `double` | double-precision real | 8 bytes | `%lf` |
| `void` | no value (functions without a return value) | none | |

The modifiers `short`, `long`, `signed`, `unsigned` change the size or range (`long int`, `unsigned char`). Derived types (arrays, pointers, structures, unions) and enumerated types are built from these.

**Precedence and associativity of operators.** **Precedence** decides *which operator is evaluated first* in an expression with several different operators; **associativity** decides the *order of evaluation among operators of the same precedence* (left to right or right to left).

| Precedence (high to low) | Operators | Associativity |
|---|---|---|
| 1 | `()` `[]` `.` `->` postfix `++ --` | left to right |
| 2 | unary `+ -` `!` `~` prefix `++ --` `*` (deref) `&` `sizeof` | right to left |
| 3 | `*` `/` `%` | left to right |
| 4 | `+` `-` | left to right |
| 5 | `<<` `>>` | left to right |
| 6 | `<` `<=` `>` `>=` | left to right |
| 7 | `==` `!=` | left to right |
| 8-10 | `&`, `^`, `\|` | left to right |
| 11-12 | `&&`, `\|\|` | left to right |
| 13 | `?:` | right to left |
| 14 | `=` `+=` `-=` `*=` ... | right to left |
| 15 | `,` | left to right |

*Examples.* (i) Precedence: `x = 2 + 3 * 4;` multiplication binds tighter than addition, so $x = 2+12 = 14$ (not $20$). (ii) Associativity (left to right): `x = 20 / 5 * 2;` gives $(20/5)\times2 = 8$ and `10 - 4 - 3` gives $(10-4)-3 = 3$. (iii) Associativity (right to left): `a = b = c = 5;` is `a = (b = (c = 5))`, so all three become $5$. Parentheses override both rules: `(2 + 3) * 4 = 20`.

**b) Output.** Take $n = 90$ (every format ends with a blank before the newline):

| Statement | Meaning of the format | Output (`_` = blank) |
|---|---|---|
| `printf("%10d \n", n);` | width $10$, right-justified | `________90_` (8 blanks, `90`, one blank) |
| `printf("%-2d \n", n);` | width $2$ equals the digits, left-justified | `90_` |
| `printf("%c \n", 'A');` | character | `A_` |
| `printf("%-10d \n", n);` | width $10$, left-justified | `90_________` (`90`, 8 blanks, one blank) |

Run output (blanks shown as they are printed):

```text
        90 
90 
A 
90         
```

@s 3
**Else-if ladder vs switch.**

| else-if ladder | switch statement |
|---|---|
| Tests **any logical or relational condition**: ranges, floats, several variables (`if (x > 5 && y < 3)`) | Compares **one integer or character expression** with **constant** case values only (no ranges, no real numbers, no conditions) |
| Conditions are evaluated one after another from the top; the first true one is run | Control jumps **directly** to the matching `case`, so it is faster for many choices |
| The `else` clause handles the rest | The `default` label handles the rest |
| No `break` is needed (only one branch runs) | `break` is needed, otherwise **fall through** to the next case |
| More readable for a few conditions; long ladders become clumsy | More readable and neat for a multi-way choice, e.g. menus |
| Syntax: `if (c1) {...} else if (c2) {...} else {...}` | Syntax: `switch (e) { case 1: ... break; default: ... }` |

**Palindrome program.** Reverse the number and compare with the original:

{{palc.c}}

Sample: `12321` gives `12321 is a palindrome` ($12321$ reversed is $12321$); `1234` gives `1234 is not a palindrome` ($4321\neq1234$).

@s 4
**Syntax of function prototypes for arrays.**

- **1-D array:** `return_type function_name(data_type array_name[], int size);` or `data_type *array_name`, e.g. `void display(int s[], int n);` The array is called as `display(sum, n);`.
- **2-D array:** every dimension **except the first must be given**: `return_type function_name(data_type array_name[][COLS], int rows, int cols);`, e.g. `void colSum(int a[][10], int m, int n, int sum[]);` The call is `colSum(a, m, n, sum);`.

Only the address of the first element is passed, so the function works on the original array.

**Program.** The 2-D array of any size up to $10\times10$ is read, `colSum()` adds each column into the 1-D array `sum[]`, and `display()` prints it:

{{colsum.c}}

Test: a $2\times3$ array with elements `1 2 3 4 5 6` (rows $1,2,3$ and $4,5,6$) gives `Column sums: 5 7 9`.

@s 5
In a **16-bit compiler** an `int` holds only up to $32767$, so the **six-digit roll number** is declared `long` ($999999$ needs $4$ bytes). Marks of five subjects are kept in an array of the structure; the total and percentage (each subject out of $100$, so percentage $=\text{total}/5$) are computed per student:

{{stud.c}}

Test, $N = 2$:

```text
Name         Roll    Marks                     Total  Percent
Ram          123456   70  80  90  60  75   375    75.00%
Sita         234567   88  92  79  85  90   434    86.80%
```

(Roll numbers are printed with `%06ld` so that leading zeros are kept.)

@s 6
**a) Call by value vs call by reference.**

| Call by value | Call by reference (address) |
|---|---|
| The **values** of the actual arguments are **copied** to the formal parameters | The **addresses** of the actual arguments are passed to pointer parameters |
| Changes in the function **do not affect** the caller's variables | Changes made through the pointers **do affect** the caller's variables |
| Separate memory for the copies | The same memory location is shared |
| Call `swap(a, b);`, definition `void swap(int x, int y)` | Call `swap(&a, &b);`, definition `void swap(int *x, int *y)` |
| Only one value can be returned (`return`) | More than one value can be modified or returned |

```c
void swapVal(int x, int y)   { int t = x; x = y; y = t; }
void swapRef(int *x, int *y) { int t = *x; *x = *y; *y = t; }
/* a = 5, b = 9:  swapVal(a, b) leaves a = 5, b = 9;  swapRef(&a, &b) gives a = 9, b = 5 */
```

**b) Output.** Here `ptr1 = &a` (so `ptr1` holds $6422296$) and `ptr2 = &ptr1` (so `ptr2` holds $6422292$):

| Statement | Values printed |
|---|---|
| `printf("%d\t %d \n", a, &a)` | $a = 10$ and the address of $a$, $6422296$ |
| `printf("%d\t %d \n", &ptr1, ptr1)` | the address of `ptr1`, $6422292$, and its content $6422296$ |
| `printf("%d\t %d \n", *ptr1, *ptr2)` | `*ptr1` $= a = 10$; `*ptr2` $=$ `ptr1` $= 6422296$ |
| `**ptr2 = 20;` then `printf("%d", a)` | `**ptr2` is `a`, so $a$ becomes $20$ |

```text
10	 6422296 
6422292	 6422296 
10	 6422296 
20
```

(The addresses are the ones printed in the question's table.) Filling in the memory table (the **Value** column; $a$ is shown after the assignment `**ptr2 = 20`):

| Variable | Value | Address |
|---|---|---|
| a | $10$ at first, then $20$ | $6422296$ |
| ptr1 | $6422296$ (address of $a$) | $6422292$ |
| ptr2 | $6422292$ (address of ptr1) | $6422280$ |

@s 7
**String handling functions.** A string in C is a character array ending with the null character `'\0'`; the operations on it are done by the library functions declared in `<string.h>`:

| Function | Purpose | Example |
|---|---|---|
| `strlen(s)` | length of the string (without `'\0'`) | `strlen("Nepal")` is $5$ |
| `strcpy(d, s)` | copy `s` into `d` | `strcpy(a, "Ram");` |
| `strncpy(d, s, n)` | copy at most $n$ characters | |
| `strcat(d, s)` | append `s` to the end of `d` | `strcat(a, b);` |
| `strcmp(s1, s2)` | compare: $0$ if equal, $<0$ if `s1<s2`, $>0$ if `s1>s2` | `strcmp("a","b")` is negative |
| `strrev(s)`, `strlwr(s)`, `strupr(s)` | reverse, lower case, upper case (non-standard, Turbo C) | |
| `strchr(s, c)`, `strstr(s, t)` | find a character or substring | |

**Program (no string functions).** Move to the end of the first string and copy the second one character by character, then put the terminating null:

{{concat.c}}

Test: first string `hello`, second string `world` gives `Concatenated string: helloworld` (`s1` must be large enough to hold both, here $100$ characters).

@s 8
A structure `book` with the members name, price and author; one record is entered by the user, written to `book.txt` with `fprintf()`, then read back with `fscanf()` and displayed:

{{book.c}}

Test: input `Alchemist 450.50 Coelho` writes the line `Alchemist 450.50 Coelho` into `book.txt` and prints

```text
Record read from book.txt
Name   : Alchemist
Price  : 450.50
Author : Coelho
```

(`%s` reads up to a blank, so names with blanks are written with underscores; a full line can be read with `fgets()`.)

@s 9
**Control structures in C and FORTRAN.** Control structures decide the order in which statements are executed.

| Type | C | FORTRAN (77 / 90) |
|---|---|---|
| **Sequence** | statements run in order | statements run in order |
| **Selection (decision)** | `if`, `if-else`, else-if ladder, nested if, `switch-case`, conditional operator `?:` | logical `IF (cond) statement`; block `IF (cond) THEN ... ELSE IF ... ELSE ... END IF`; **arithmetic IF** `IF (e) l1,l2,l3` (3-way); computed `GO TO (l1,l2,l3), i`; `SELECT CASE` (F90) |
| **Iteration (loops)** | `for`, `while` (entry-controlled), `do-while` (exit-controlled) | `DO label i = start, end, step ... label CONTINUE` (counted loop), `DO WHILE (cond) ... END DO` (F90), `DO ... EXIT ... END DO` |
| **Jump** | `break` (leave loop or switch), `continue` (next iteration), `goto label`, `return` | `GO TO label`, `EXIT`, `CYCLE` (F90), `STOP`, `RETURN` |

*Examples.*

```c
for (i = 1; i <= 5; i++)        /* C counted loop */
    sum += i;
```
```fortran
      DO 10 I = 1, 5
         SUM = SUM + I
   10 CONTINUE
```

*Main differences:* (i) C has **three** loop forms (`for`, `while`, `do-while`) with the test written by the programmer, while the FORTRAN `DO` loop is a **counted loop** whose trip count is fixed when the loop starts and whose control variable cannot be changed inside the loop; (ii) the test of the `if` in C is any **non-zero (true) expression**, while FORTRAN needs a **logical expression** (`.GT.`, `.EQ.`, `.AND.`); (iii) C has `switch` (integers and characters) whereas FORTRAN 77 has no `switch` (computed `GO TO`, `SELECT CASE` in F90); (iv) FORTRAN has the **arithmetic IF** with three labels, and C has no equivalent; (v) in C blocks use `{ }`, in FORTRAN they end with `END IF`, `END DO` or a labelled `CONTINUE`; (vi) the C `break`/`continue` correspond to FORTRAN 90 `EXIT`/`CYCLE`.

@s 10
**Method.** The $100$ numbers are read into an array and sorted by the **bubble sort**: in each pass adjacent elements are compared and exchanged if the first is larger, so the largest element goes to the end; $99$ passes sort the array.

```fortran
{{sort.f90}}
```

Compiled with gfortran and tested with $100$ random integers: the smallest values are printed first, `3.0 10.0 23.0 23.0 27.0 ...` and the last `... 991.0 993.0 997.0`, in agreement with Python's `sorted()`. The numbers can be typed on one or several lines (list-directed input). Using the inner limit `N - I` avoids comparing the part already sorted. (For a descending order change `.GT.` to `.LT.`.)
