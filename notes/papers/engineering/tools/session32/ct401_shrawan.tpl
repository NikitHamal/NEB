---
file: NEBians-IOE-Past-Paper-Computer-Programming-CT401-2082-Shrawan.pdf
subject: Computer Programming
level: BE · Year I / Part I
code: CT 401
year_bs: 2082 Shrawan
cal: BS
year_ad: 2025
stream: All programmes except B.Arch and BAS
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Batch-out paper (old course, CT 401). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Define instruction and program. Discuss in brief about different generations of programming languages. [[1+3]]

b) Explain the importance of problem analysis in software development. Write an algorithm and draw a flowchart to test whether a number entered by the user is even or not. [[1+3]]

@q 2
a) What is an expression? What are the types of expression? [[2+2]]

b) Explain about input and output functions available in C with syntax and example of each part. [[2+2+2]]

@q 3
a) Compare nested if with else if ladder structure along with their flowchart. [[4]]

b) Write a program to check whether a number entered by the user is prime or composite. [[4]]

@q 4
a) What do you mean by "call by value and call by reference"? Explain it with a suitable example. [[4]]

b) Write a program to display the factorial of an integer entered by the user using the concept of a recursive function. [[4]]

@q 5
a) Write a program to reverse a string without using string handling functions. [[4]]

b) Write a program to display the largest and smallest number among 10 numbers entered by the user. [[6]]

@q 6
What is structure? Why is it necessary? Write a program to add two distances given in feet and inch format using structure. [[1+1+6]]

@q 7
a) Explain pointer arithmetic with a suitable example. [[4]]

b) Write a program to display the sum, difference and product of two numbers using the concept of pointer. [[4]]

@q 8
Differentiate between console I/O and file I/O. A file named "employee.txt" stores employee name, employee id and employee salary. Write a program to display the details of all employees having salary greater than 50000. [[2+6]]

@q 9
List down the key differences between C and FORTRAN. How are one-dimensional and two-dimensional arrays declared in FORTRAN? Write a program in FORTRAN to read and compute the transpose of any matrix. [[2+4+6]]
<!-- SOLUTIONS -->

@s 1
**a) Instruction and program.** An **instruction** is a single command given to the computer's processor, telling it to perform one primitive operation (for example `ADD`, `MOV`, or a C statement such as `c = a + b;`). A **program** is a finite, ordered set of instructions written in a programming language to solve a particular problem or to perform a task.

**Generations of programming languages.**

| Generation | Language | Description | Examples |
|---|---|---|---|
| 1GL | **Machine language** | Binary instructions (0s and 1s) executed directly by the CPU; fastest, but very hard to write and machine dependent | `10110000 01100001` |
| 2GL | **Assembly language** | Mnemonics (ADD, MOV, JMP) instead of binary; translated by an **assembler**; still machine dependent | 8085, 8086 assembly |
| 3GL | **High-level languages** | English-like, procedure-oriented, machine independent; translated by a **compiler** or **interpreter** | FORTRAN, COBOL, C, C++, Java, Python |
| 4GL | **Very high-level (non-procedural) languages** | The programmer says *what* is wanted rather than *how*; used for databases, reports and GUIs; much less code | SQL, MATLAB, report generators |
| 5GL | **Artificial intelligence and constraint-based languages** | The problem is stated as constraints and the system solves it; used in expert systems and NLP | Prolog, Mercury, OPS5 |

Each generation is closer to human language and further from the machine hardware than the last.

**b) Importance of problem analysis.** Problem analysis is the first step of the software development cycle: understanding what the problem is, what the **inputs, outputs and processing** are, and the constraints, before any code is written. It is important because it

- ensures the program solves the **right problem** and meets the user's requirements;
- avoids rework: errors found at the analysis stage cost far less to fix than errors found after coding or deployment;
- leads to a correct **algorithm and flowchart**, so that the design (choice of data structures, modules) is sound;
- helps estimate time, cost and resources, makes testing easier (known inputs and expected outputs) and documentation clearer.

**Algorithm (even or odd).**

1. Start.
2. Read the number $n$.
3. If $n \bmod 2 = 0$ then print "Even", else print "Odd".
4. Stop.

{{FIG:evenodd|Question 1(b): flowchart to test whether the number entered by the user is even or odd.}}

@s 2
**a) Expression.** An **expression** is a combination of operands (constants, variables, function calls) and operators that the compiler evaluates to a single value, for example `a + b * 2`, `x > y`, `(a > b) ? a : b`.

**Types of expression.**

| Type | Meaning | Example |
|---|---|---|
| Arithmetic | Uses `+ - * / %`; result is integer or real | `a * b + c / 2` |
| Relational | Compares two values with `< > <= >= == !=`; result is 1 (true) or 0 (false) | `a > b` |
| Logical | Combines conditions with `&& \|\| !` | `(a > 0) && (b > 0)` |
| Assignment | Stores a value in a variable | `x = y + 5` |
| Conditional | `condition ? expr1 : expr2` | `max = (a > b) ? a : b` |
| Bitwise | Operates on bits: `& \| ^ ~ << >>` | `a & 0x0F` |
| Increment / decrement | `++`, `--` | `i++` |

Depending on the position of the operator, expressions may be **infix** ($a+b$), **prefix** ($+ab$) or **postfix** ($ab+$); and by the type of the result they may be integer, real (float) or pointer expressions.

**b) Input and output functions in C.** They are in the header `<stdio.h>`.

*1. Formatted I/O*: `scanf()` and `printf()` read and write data of the stated type using format specifiers (`%d`, `%f`, `%c`, `%s`).

- Syntax: `scanf("format string", &variable1, &variable2, ...);` and `printf("format string", expr1, expr2, ...);`
- Example:

```c
int a; float b;
scanf("%d %f", &a, &b);
printf("a = %d, b = %.2f\n", a, b);
```

*2. Character I/O (unformatted)*: `getchar()`, `putchar()`, `getch()`, `getche()`, `putch()` read or write one character at a time.

- Syntax: `ch = getchar();` and `putchar(ch);`
- Example:

```c
char ch;
ch = getchar();     /* reads one character from the keyboard */
putchar(ch);        /* displays it */
```

*3. String I/O (unformatted)*: `gets()` / `fgets()` and `puts()` read and write a whole line (a string including spaces).

- Syntax: `gets(str);` (unsafe, use `fgets(str, size, stdin);`) and `puts(str);`
- Example:

```c
char name[40];
fgets(name, 40, stdin);   /* reads a line */
puts(name);               /* prints it and a newline */
```

@s 3
**a) Nested if versus else-if ladder.**

| Nested if | else-if ladder |
|---|---|
| An `if` (or `else`) statement contains another `if` statement inside it | A chain of `if ... else if ... else if ... else` at the same level |
| The inner condition is tested **only if the outer condition is true** (a decision tree); used when decisions depend on one another | The conditions are tested **one after the other from the top** until one is true; the rest are skipped; used for **multi-way selection** among exclusive alternatives |
| Indentation grows with depth, so it is harder to read | Flat structure, easier to read and maintain |
| Example: check `a > 0`, and inside it check `b > 0` | Example: grade from marks (`>= 80`, `>= 60`, `>= 40`, else) |
| Syntax: `if (c1) { if (c2) S1; else S2; } else S3;` | Syntax: `if (c1) S1; else if (c2) S2; else if (c3) S3; else S4;` |

{{FIG:nested|Question 3(a): flowchart of a nested if: the inner decision is tested only when the outer condition is true.}}

{{FIG:ladder|Question 3(a): flowchart of the else-if ladder: conditions are tested in order until one is true, otherwise the last else part executes.}}

**b) Prime or composite.** A prime number is greater than 1 and divisible only by 1 and itself; a number greater than 1 that is not prime is composite. It is enough to test divisors up to $\sqrt n$.

{{C:prime.c}}

Sample runs: for input `29` the output is `29 is a prime number`; for input `91` it is `91 is a composite number` ($91 = 7\times13$).

@s 4
**a) Call by value and call by reference.**

- **Call by value:** the **value** of the actual argument is copied to the formal parameter. The function works on its own copy, so changes made inside the function **do not affect** the actual arguments in the caller.
- **Call by reference:** the **address** of the actual argument is passed (using pointers). The function works on the original variable through its address, so changes **are reflected** in the caller.

{{C:swapcmp.c}}

Output (both functions swap their own parameters, but only the call by reference changes `x` and `y` in `main`):

```text
Inside swapByValue : a = 20, b = 10
After call by value    : x = 10, y = 20
Inside swapByReference: a = 20, b = 10
After call by reference: x = 20, y = 10
```

**b) Factorial using recursion.** $n! = n\times(n-1)!$ with $0! = 1! = 1$. A recursive function calls itself with a smaller argument until the base case is reached.

{{C:fact.c}}

Sample: input `6` gives `Factorial of 6 = 720`. (`unsigned long long` holds up to $20!$.)

@s 5
**a) Reverse a string without string-handling functions.**

{{C:revstr.c}}

Sample: `Hello NEB` gives `Reversed string: BEN olleH`.

**b) Largest and smallest of 10 numbers.** The first number initialises both the largest and the smallest; each later number is compared with them.

{{C:maxmin.c}}

Sample: for `4 9 -2 7 15 3 0 8 11 6` the output is `Largest  = 15` and `Smallest = -2`.

@s 6
**Structure.** A **structure** is a user-defined data type that groups **variables of different data types** under a single name, declared with the keyword `struct`; its members are accessed with the dot operator (`d1.feet`).

**Why it is necessary.** Real-world entities (a student, an employee, a distance) have attributes of different types (name, roll number, marks). An array can hold only one type, and separate variables are hard to manage, copy and pass to functions. A structure keeps related data together as one unit, so that records can be created, assigned, passed to functions and stored in arrays (and in files) easily, which makes the program organised and readable.

**Program: adding two distances in feet and inch** (12 inch = 1 foot):

{{C:dist.c}}

Sample: `5 8.5` and `3 6.5` give `Sum = 9 feet 3.0 inch` ($8.5 + 6.5 = 15$ inch $= 1$ ft $3$ inch).

@s 7
**a) Pointer arithmetic.** A pointer holds a memory address, and only a few arithmetic operations are meaningful on it:

- **Increment / decrement** (`p++`, `p--`): moves the pointer to the next / previous element: the address changes by `sizeof(type)` bytes (4 for `int`).
- **Adding or subtracting an integer** (`p + n`, `p - n`): gives the address of the element $n$ places away, i.e. $\text{address} + n\times\text{sizeof(type)}$.
- **Subtracting two pointers** of the same array (`q - p`): gives the number of elements between them.
- **Comparison** (`<`, `>`, `==`) of pointers to the same array.
- Adding, multiplying or dividing two pointers is **not allowed**.

{{C:ptrarith.c}}

Output (addresses vary from run to run; the step is 4 bytes for `int`):

```text
*p = 10, p = 0x7ffd4a2c1e20
after p++ : *p = 20, p = 0x7ffd4a2c1e24
after p+2 : *p = 40, p = 0x7ffd4a2c1e2c
q - p = 1 elements
*(a + 3) = 40
```

**b) Sum, difference and product using pointers.**

{{C:ptrops.c}}

Sample: inputs `12 5` give `Sum = 17`, `Difference = 7`, `Product = 60`.

@s 8
**Console I/O vs file I/O.**

| Console I/O | File I/O |
|---|---|
| Data are read from the keyboard and written to the monitor (standard input/output) | Data are read from and written to a **disk file** |
| Uses `printf`, `scanf`, `getchar`, `putchar`, `gets`, `puts` | Uses `fopen`, `fclose`, `fprintf`, `fscanf`, `fgetc`, `fputc`, `fgets`, `fputs`, `fread`, `fwrite` |
| Data are **temporary** (lost when the program ends) | Data are **permanent** (persist after the program ends) |
| Suitable for small amounts of data | Suitable for large amounts of data; can be reused by other programs |
| No file pointer needed | Needs a `FILE *` pointer and the file opened/closed explicitly |

**Program.** Each line of `employee.txt` has the form `name id salary` (for example `Ram 101 45000`).

{{C:emp.c}}

For a file containing

```text
Ram 101 45000
Sita 102 62000
Hari 103 50000
Gita 104 75500.50
```

the output is

```text
Name            ID     Salary
Sita            102    62000.00
Gita            104    75500.50
```

(Hari's salary is exactly 50000, which is not greater than 50000.)

@s 9
**Key differences between C and FORTRAN.**

| C | FORTRAN |
|---|---|
| General-purpose, structured, middle-level language for system and application programming | Scientific and numerical computing language (FORmula TRANslation), designed for engineers and scientists |
| Case sensitive; free-form code; statements end with `;` | Not case sensitive; (fixed form: columns 7-72, one statement per line); no `;` terminator |
| Arrays are indexed from **0**; stored row-major | Arrays are indexed from **1** by default; stored **column-major** |
| Pointers, structures, dynamic memory, bit operations are supported | Built-in complex numbers, powerful array operations and the `**` power operator; no pointers in FORTRAN 77 |
| Call by value for arguments | Call by **reference** for arguments |
| Many control structures (`for`, `while`, `do-while`, `switch`) | `DO` loops, `IF` / arithmetic `IF`, `GO TO`, `SELECT CASE` (F90) |
| Standard library is small and I/O is by functions (`printf`) | I/O by `READ`/`WRITE` statements with `FORMAT` |

**Declaring arrays in FORTRAN.**

```fortran
INTEGER A(10)            ! one-dimensional: 10 elements A(1) ... A(10)
REAL    B(3,4)           ! two-dimensional: 3 rows, 4 columns
DIMENSION C(5,5)         ! DIMENSION statement (type from implicit rule)
REAL, DIMENSION(10) :: x ! Fortran 90 style
```

The general form is `type name(size)` for 1-D and `type name(rows, columns)` for 2-D; subscripts start from 1 (a different lower bound can be given as `A(0:9)`).

**Program: transpose of a matrix** (Fortran 90 with an allocatable array, so any size $m\times n$ can be used):

{{F:transpose.f90}}

Sample run with $m = 2$, $n = 3$ and the matrix $\begin{pmatrix}1&2&3\\4&5&6\end{pmatrix}$ gives

```text
 Transpose of the matrix:
    1.00    4.00
    2.00    5.00
    3.00    6.00
```
