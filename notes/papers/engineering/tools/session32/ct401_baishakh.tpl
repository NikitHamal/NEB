---
file: NEBians-IOE-Past-Paper-Computer-Programming-CT401-2082-Baishakh.pdf
subject: Computer Programming
level: BE · Year I / Part I
code: CT 401
year_bs: 2082 Baishakh
cal: BS
year_ad: 2025
stream: All programmes except B.Arch and BAS
time: 3 hrs
marks: 80
students: Tribhuvan University, Institute of Engineering, Examination Control Division. Back paper (old course, CT 401). Pass marks 32.
category: University Exam
---
<small>Candidates are required to give their answers in their own words as far as practicable · Attempt all questions · The figures in the margin indicate full marks · Assume suitable data if necessary</small>

@q 1
a) Differentiate between system software and application software. [[2]]

b) Why is the C programming language most commonly used in simulation? [[2]]

@q 2
a) What do you understand by testing and debugging? [[2]]

b) Write an algorithm and draw a flowchart to find the sum of the first $n$ natural numbers where the value of $n$ is entered by the user. [[4]]

@q 3
a) Define precedence and associativity of operators with examples. [[2]]

b) Define keywords. List down the rules for writing identifiers in C. [[2]]

@q 4
Differentiate between unformatted and formatted input/output in C. [[4]]

@q 5
a) Write a program in C to check whether a number entered by the user is prime or composite. [[5]]

b) Write a program in C to display the following pattern: [[5]]

```text
                *
            *   *   *
        *   *   *   *   *
    *   *   *   *   *   *   *
*   *   *   *   *   *   *   *   *
```

@q 6
a) Define functions and classify them. List down the advantages of using functions in the program. [[2]]

b) Write a program in C to display the $n^{th}$ term of the Fibonacci sequence using a recursive function. The value of $n$ is entered by the user. [[6]]

@q 7
a) Define 1D and 2D array. Write a program in C to display the transpose of an $m\times n$ matrix entered by the user. [[2+4]]

b) Write a program in C to calculate the length of a string entered by the user without using the library function. [[4]]

@q 8
Define nested structure. Write a program in C to input the name, roll, marks and address of $n$ students from the user and display the entered details in the order of marks. [[2+6]]

@q 9
a) Define pointers. List out the importance of pointers in C programming. [[1+2]]

b) Write a program in C to sort $n$ numbers entered by the user in ascending order using the concept of pointers. [[5]]

@q 10
Differentiate between text file and binary file. Write a program in C to copy the contents of a file "source.txt" into "destination.txt". [[2+6]]

@q 11
Describe the structure of a FORTRAN program. List down the data types available in FORTRAN. Write a program in FORTRAN to determine whether the number entered by the user is negative, zero or positive using the concept of arithmetic IF. [[2+2+6]]
<!-- SOLUTIONS -->

@s 1
**a) System software vs application software.**

| System software | Application software |
|---|---|
| Manages and controls the computer hardware and provides a platform to run other software | Performs specific tasks for the user |
| Runs in the background, starts when the computer boots and runs until it shuts down | Runs only when the user starts it |
| Written in low-level languages (C, assembly) and is hard to design | Written in high-level languages and easier to develop |
| General purpose; the computer cannot work without it | Special purpose; not needed for the computer to function |
| Examples: operating systems (Linux, Windows), device drivers, compilers, assemblers, utility programs | Examples: word processors, spreadsheets, browsers, media players, payroll and accounting software |

**b) Why C is used in simulation.** C is widely used for simulation (engineering and scientific models, network, circuit and physical simulators) because it

- produces **fast, efficient, compact code** that runs close to the hardware, which matters when a model has millions of iterations;
- gives **direct memory and hardware control** by pointers and bit operations, and **dynamic memory allocation** for large data sets;
- is **portable** (compilers on every platform) and **structured/modular**, so large models are built from functions and libraries;
- has a **rich set of operators**, a large library of numerical routines and it interfaces easily with other languages and hardware.

@s 2
**a) Testing and debugging.**

- **Testing** is the process of **executing a program with sample (test) data to find the errors** and to check that the output matches the requirement (unit, integration, system and acceptance tests; black-box and white-box methods). It *detects* the presence of errors.
- **Debugging** is the process of **locating the cause of the errors found, and correcting them**: by tracing, inserting print statements, using breakpoints and watching variables in a debugger. Types of errors: syntax (compile-time), runtime and logical errors.

Testing finds the bug; debugging removes it.

**b) Sum of the first $n$ natural numbers.**

*Algorithm:*

1. Start.
2. Read $n$.
3. Set sum $= 0$ and $i = 1$.
4. While $i\le n$: sum $=$ sum $+\ i$ and $i = i + 1$.
5. Print sum.
6. Stop.

{{FIG:sumn|Question 2(b): flowchart for the sum of the first n natural numbers.}}

For $n = 5$: sum $= 1+2+3+4+5 = 15$ (also $n(n+1)/2$).

@s 3
**a) Precedence and associativity.**

- **Precedence** decides **which operator is evaluated first** in an expression containing different operators: an operator of higher precedence is evaluated before one of lower precedence. Example: in `a + b * c` the `*` has higher precedence than `+`, so it is evaluated as `a + (b * c)`; with `a = 2, b = 3, c = 4` the value is $14$ and not $20$.
- **Associativity** decides **the order of evaluation among operators of the same precedence**: left-to-right or right-to-left. Example: `10 - 4 - 3` is evaluated left to right as `(10 - 4) - 3 = 3`; the assignment `a = b = 5` is right to left as `a = (b = 5)`.

| Precedence (high to low) | Operators | Associativity |
|---|---|---|
| 1 | `() [] -> .` | left to right |
| 2 | `! ~ ++ -- + - (type) * & sizeof` (unary) | right to left |
| 3 | `* / %` | left to right |
| 4 | `+ -` | left to right |
| 5 | `< <= > >=`, then `== !=` | left to right |
| 6 | `&&`, then `\|\|` | left to right |
| 7 | `?:`, then `= += -= ...` | right to left |

**b) Keywords and identifier rules.** **Keywords** are the **reserved words** of the language that have a fixed, predefined meaning for the compiler and cannot be used as identifiers, e.g. `int`, `float`, `char`, `if`, `else`, `for`, `while`, `return`, `struct`, `void` (C has 32 keywords in ANSI C).

**Rules for identifiers** (names of variables, functions, arrays, etc.):

1. They may contain letters (`a-z`, `A-Z`), digits (`0-9`) and the underscore `_` only.
2. The first character must be a letter or an underscore, **not a digit**.
3. No spaces or special characters (such as `@ # $ % -`) are allowed.
4. A keyword cannot be used as an identifier.
5. C is **case sensitive** (`Total` and `total` are different) and the name should be unique in its scope; the first 31 characters are significant.

@s 4
**Unformatted vs formatted input/output.**

| Formatted I/O | Unformatted I/O |
|---|---|
| Data are read or written **in a specified format** using **format specifiers** (`%d`, `%f`, `%c`, `%s`) | Data are read or written **without any format**, as raw characters or strings |
| Functions: `scanf()`, `printf()` (and `fscanf`, `fprintf` for files) | Functions: `getchar()`, `putchar()`, `getch()`, `getche()`, `putch()`, `gets()`, `puts()` |
| Can handle all data types (int, float, char, string) in one call and control width/precision (`%6.2f`) | Handle only a character or a string at a time; no control over the output format |
| `scanf` stops reading at whitespace; `printf` can print several values at once | `gets` reads a complete line including spaces |
| Example: `scanf("%d", &n); printf("%5.2f", x);` | Example: `ch = getchar(); putchar(ch); puts(str);` |

@s 5
**a) Prime or composite.**

{{C:prime.c}}

Sample: `29` gives `29 is a prime number`; `91` gives `91 is a composite number`.

**b) Pattern program.** In row $i$ ($i = 1,\dots,5$) there are $(rows - i)$ leading blanks of width 2 and then $2i-1$ stars separated by a blank, giving a pyramid with $1,3,5,7,9$ stars.

{{C:pyramid.c}}

Output:

```text
        * 
      * * * 
    * * * * * 
  * * * * * * * 
* * * * * * * * * 
```

@s 6
**a) Function.** A **function** is a self-contained block of statements that performs a specific task, is given a name, and can be called any number of times from other parts of the program (`return_type name(parameters) { body }`).

**Classification.**

1. *By origin:* **library (built-in) functions** (`printf`, `sqrt`, `strlen`) and **user-defined functions**.
2. *By arguments and return value:* (i) no arguments, no return value; (ii) arguments, no return value; (iii) no arguments, return value; (iv) arguments and return value.
3. *By calling:* call by value and call by reference; and recursive functions (a function calling itself).

**Advantages.** Modular programming (a big problem is broken into small parts), **reusability** (written once, used many times), reduction of code size and repetition, easier **debugging and testing**, easier maintenance and understanding, team development of different functions, and the ability to build libraries.

**b) $n$th Fibonacci term by recursion.** The sequence $0, 1, 1, 2, 3, 5, 8, 13,\dots$ with $F_1 = 0$, $F_2 = 1$, $F_n = F_{n-1} + F_{n-2}$.

{{C:fib.c}}

Sample: input `7` gives `The 7th term of the Fibonacci sequence = 8` (sequence $0,1,1,2,3,5,8$).

@s 7
**a) Arrays.**

- A **one-dimensional (1D) array** is a collection of elements of the **same data type** stored in contiguous memory locations and accessed by a single subscript: `int a[5];` with elements `a[0]` to `a[4]`.
- A **two-dimensional (2D) array** is an array of arrays, a table of rows and columns accessed by two subscripts: `int a[3][4];` (3 rows, 4 columns), element `a[i][j]`.

**Transpose of an $m\times n$ matrix.** The transpose $T$ is $n\times m$ with $t_{ji} = a_{ij}$.

{{C:trans.c}}

Sample: for $m = 2$, $n = 3$ and elements `1 2 3 4 5 6`:

```text
Transpose (3 x 2):
   1   4
   2   5
   3   6
```

**b) Length of a string without the library function.** The string ends with the null character `'\0'`; count the characters before it.

{{C:strlen2.c}}

Sample: `Nepal Engineering` gives `Length of the string = 17`.

@s 8
**Nested structure.** A structure that contains **another structure as a member** is called a nested structure. Here the `Address` structure is a member of the `Student` structure; the inner members are reached with two dots (`s[i].addr.city`).

**Program.** Records are read for $n$ students and sorted in **descending order of marks** (bubble sort on the structure array) before display. (For ascending order change `<` to `>` in the comparison.)

{{C:nested.c}}

Sample (3 students):

```text
Name       Roll  Marks  Address
Sita       2     88.0   Pokhara, Gandaki
Ram        1     72.5   Kathmandu, Bagmati
Hari       3     65.0   Butwal, Lumbini
```

@s 9
**a) Pointer.** A **pointer** is a variable that stores the **memory address of another variable** (`int *p = &x;`); `*p` accesses the value at that address (dereferencing).

**Importance of pointers.**

1. **Dynamic memory allocation** (`malloc`, `calloc`, `free`) for arrays and data structures of run-time size.
2. **Call by reference**: functions can change the caller's variables and return more than one value.
3. Efficient handling of **arrays and strings** (pointer arithmetic) and passing large arrays or structures without copying.
4. Building **linked lists, trees, graphs** and other dynamic data structures.
5. Direct access to memory and hardware (system programming) and pointers to functions (callbacks).

**b) Sort $n$ numbers using a pointer** (bubble sort; every element is accessed as `*(p + j)`):

{{C:ptrsort.c}}

Sample: `n = 6`, numbers `42 7 19 3 88 25` gives `Sorted (ascending): 3 7 19 25 42 88`.

@s 10
**Text file vs binary file.**

| Text file | Binary file |
|---|---|
| Stores data as **ASCII (readable) characters**, line by line | Stores data in **binary form (0s and 1s)**, exactly as in memory |
| Can be opened and read in any text editor | Not human readable; needs the program that wrote it |
| Newline is translated (`\n` becomes CR LF on Windows) | No translation takes place |
| Takes more space (a number `12345` takes 5 bytes) and is slower to read/write | Compact (an `int` always takes 4 bytes) and faster |
| Modes `"r"`, `"w"`, `"a"`; functions `fprintf`, `fscanf`, `fgets`, `fputs` | Modes `"rb"`, `"wb"`, `"ab"`; functions `fread`, `fwrite` |
| Examples: `.txt`, `.c` | Examples: `.exe`, `.jpg`, `.dat` |

**Program to copy `source.txt` into `destination.txt`** (character by character; `ch` is an `int` so that `EOF` can be detected):

{{C:fcopy.c}}

If `source.txt` contains `Hello NEB` and `Second line`, `destination.txt` gets exactly the same two lines and the program prints `File copied successfully`.

@s 11
**Structure of a FORTRAN program.** A (FORTRAN 77, fixed-form) program consists of:

1. **Program heading** (optional): `PROGRAM name`.
2. **Specification (declaration) part:** type declarations (`INTEGER`, `REAL`), `DIMENSION`, `PARAMETER`, `COMMON`, `IMPLICIT NONE`.
3. **Executable part:** assignment statements, `READ`/`WRITE`, control statements (`IF`, `DO`, `GO TO`) and calls to subprograms.
4. **Subprograms** (optional): `FUNCTION` and `SUBROUTINE`.
5. **`STOP`** and the compulsory **`END`** statement.

Layout (fixed form): columns 1-5 statement label, column 6 continuation mark, columns 7-72 the statement, column 1 `C` or `*` for a comment.

**Data types of FORTRAN:** `INTEGER`, `REAL` (single precision), `DOUBLE PRECISION`, `COMPLEX`, `LOGICAL` and `CHARACTER`.

**Arithmetic IF.** `IF (expression) L1, L2, L3` transfers control to the statement labelled `L1` if the expression is negative, to `L2` if it is zero, and to `L3` if it is positive.

{{F:sign.f}}

Compiled with gfortran (`-std=legacy`); the runs give:

```text
 ENTER A NUMBER
-4.5
 THE NUMBER IS NEGATIVE
 ENTER A NUMBER
0
 THE NUMBER IS ZERO
 ENTER A NUMBER
7
 THE NUMBER IS POSITIVE
```
